"""Utility functions to manipulate SimulationJob."""
from google.cloud import datastore
from proto import simulation_job_pb2
import bunnieinfra.jobs.bunnie_simulation
import kubernetes.client
import kubernetes.config
import yaml

_ENTITY_KIND = "SimulationJob"
_FIELD_SIMULATION_JOB = "simulation_job"
_FIELD_JOB_STATUS = "job_status"

_BOOT_FILE_DIRECTORY = "/usr/src/mymaven/boot-file/"


class SimulationJobUtil:
  """SimulationJob utility.

  Usage example:
    datastore_client = google.cloud.datastore.Client()
    job_util = SimulationJobUtil(datastore_client)
    ready_job = job_util.get_ready_job()
  """

  def __init__(self, datastore_client):
    """Initializes SimulationJobUtil."""
    self._datastore_client = datastore_client

  def create_job(self, brokers, google_cloud_storage_bucket_name, bootstrap_file_path,
                 bootstrap_state_file_path):
    """Creates a simulation job.

    Args:
      brokers: A list of SimulationJob.Broker.
      google_cloud_storage_bucket_name: The Google Cloud Storage bucket name. This name can be
          obtained in Google Cloud Console.
      bootstrap_file_path: The file path to bootstrap file for PowerTAC simulation.
      bootstrap_state_file_path: The file path to boostrap state file for PowerTAC simulation.

    Returns:
      The unique identifier of the created simulation job.
    """
    job = simulation_job_pb2.SimulationJob()
    job.status = simulation_job_pb2.SimulationJob.STATUS_READY
    job.brokers.extend(brokers)
    job.bootstrap_file.google_cloud_storage_bucket_name = google_cloud_storage_bucket_name
    job.bootstrap_file.bootstrap_file_path = bootstrap_file_path
    job.bootstrap_file.bootstrap_state_file_path = bootstrap_state_file_path

    job_key = self._datastore_client.key(_ENTITY_KIND)
    entity = datastore.Entity(key=job_key)
    entity[_FIELD_SIMULATION_JOB] = job.SerializeToString()
    entity[_FIELD_JOB_STATUS] = simulation_job_pb2.SimulationJob.STATUS_READY

    self._datastore_client.put(entity)
    return entity.id

  def get_ready_job(self, new_job_status=simulation_job_pb2.SimulationJob.STATUS_UNKNOWN):
    """Gets a simulation job that is in ready state.

    Args:
      new_job_status: The new status of the job. If provided, then the query and update are
          performed in a single transaction.

    Returns:
      The simulation job unique identifier and the SimulationJob if there is at least one simulation
      job in READY status. None otherwise.

    Raises:
      except google.cloud.exceptions.Conflict: If too many transactions are performed on the ready
          job.
    """
    with self._datastore_client.transaction():
      query = self._datastore_client.query(kind=_ENTITY_KIND)
      query.add_filter(_FIELD_JOB_STATUS, "=", simulation_job_pb2.SimulationJob.STATUS_READY)
      results = list(query.fetch(limit=1))

      if len(results) == 0:
        return None, None

      job_entity = results[0]
      job_id = job_entity.id

      job = simulation_job_pb2.SimulationJob()
      job.MergeFromString(job_entity[_FIELD_SIMULATION_JOB])

      if new_job_status != simulation_job_pb2.SimulationJob.STATUS_UNKNOWN:
        job.status = new_job_status
        job_entity[_FIELD_SIMULATION_JOB] = job.SerializeToString()
        job_entity[_FIELD_JOB_STATUS] = new_job_status
        self._datastore_client.put(job_entity)

    return job_id, job

  def update_job_status(self, simulation_job_id, new_job_status):
    """Updates job status.

    Args:
      simulation_job_id: The unique identifier of the simulation job.
      new_job_status: The new job status.

    Raises:
      except google.cloud.exceptions.Conflict: If too many transactions are performed on the job.
    """
    with self._datastore_client.transaction():
      key = self._datastore_client.key(_ENTITY_KIND, simulation_job_id)
      job_entity = self._datastore_client.get(key)
      job_entity[_FIELD_JOB_STATUS] = new_job_status

      job = simulation_job_pb2.SimulationJob()
      job.MergeFromString(job_entity[_FIELD_SIMULATION_JOB])
      job.status = new_job_status
      job_entity[_FIELD_SIMULATION_JOB] = job.SerializeToString()

      self._datastore_client.put(job_entity)


class ScheduleJobError(Exception):
  """Exception that is raised when job scheduling has error."""
  pass


class ScheduleJobUtil:
  """Utility to schedule SimulationJob.

  Usage example:
    datastore_client = google.cloud.datastore.Client()

    kubernetes.config.load_kube_config()
    api_instance = kubernetes.client.BatchV1Api()

    job_util = SimulationJobUtil(datastore_client)
    schedule_job_util = ScheduleJobUtil(job_util, api_instance)
    schedule_job_util.schedule_job()
  """

  def __init__(self, simulation_job_util, kubernetes_batch_v1_api):
    """Initializes SimulationJobUtil."""
    self._simulation_job_util = simulation_job_util
    self._kubernetes_batch_v1_api = kubernetes_batch_v1_api

  def schedule_job(self):
    """Schedules a simulation job that is in ready state.

    The job is scheduled using Kubernetes API. After the job is scheduled, the job status is changed
    to RUNNING status. If the job scheduling failed, the job status will be changed to READY.

    Raises:
      ScheduleJobError: if no simulation job in ready status.
      kubernetes.client.rest.ApiException: If there is an exception with scheduling the job using
          Kubernetes API.
    """

    job_id, job = self._simulation_job_util.get_ready_job(
        new_job_status=simulation_job_pb2.SimulationJob.STATUS_RUNNING)
    if job_id is None or job is None:
      raise ScheduleJobError("No simulation job in ready status.")

    k_config = yaml.safe_load(bunnieinfra.jobs.bunnie_simulation._BUNNIE_SIMULATION_TEMPLATE)

    # Shell script to run server-distribution.
    boot_file_path = _BOOT_FILE_DIRECTORY + job.bootstrap_file.bootstrap_file_path
    broker_names = ','.join([broker.name for broker in job.brokers])
    k_config["spec"]["template"]["spec"]["containers"][0]["args"] = [
        "-c",
        """
        mkdir -p /usr/src/mymaven/boot-file/
        python download_blob.py \
            --bucket_name=tensile-market-235521.appspot.com \
            --source_blob_name=%s \
            --destination_file_name=boot-file/boot.xml
        if [ $? -ne 0 ] ; then
          python update_job_status.py --id=%d --status="STATUS_FAILED"
          echo "Boot file download failed"
          exit 1
        fi

        echo "Boot file downloaded successfully"

        python download_blob.py \
            --bucket_name=tensile-market-235521.appspot.com \
            --source_blob_name=%s \
            --destination_file_name=boot-file/boot.state
        if [ $? -ne 0 ] ; then
          python update_job_status.py --id=%d --status="STATUS_FAILED"
          echo "Boot state file download failed"
          exit 1
        fi

        echo "Boot state file downloaded successfully"

        mvn -Pcli -Dexec.args="--sim --brokers=%s --boot-data=boot-file/boot.xml --weather-data=boot-file/boot.state"
        if [ $? -ne 0 ] ; then
          python update_job_status.py --id=%d --status="STATUS_FAILED"
          echo "Simulation failed"
          exit 1
        fi

        if [ ! -f log/powertac-sim-0.state ] ; then
          python update_job_status.py --id=%d --status="STATUS_FAILED"
          echo "Logs do not exists after simulation"
          exit 1
        fi

        python update_job_status.py --id=%d --status="STATUS_COMPLETED"
        echo "Finish simulation"

        # Upload state logs to Google Cloud Storage
        python upload_blob.py \
            --bucket_name=tensile-market-235521.appspot.com \
            --source_file_path=log/powertac-sim-0.state \
            --destination_blob_name=powertac2018_server_logs/%d/powertac-sim-0.state
        if [ $? -ne 0 ] ; then
          echo "Upload logs failed"
          exit 1
        fi
        python update_job_status.py --id=%d --status="STATUS_STATE_LOGS_UPLOADED"
        echo "Uploaded state logs to Google Cloud Storage"
        """ % (job.bootstrap_file.bootstrap_file_path, job_id,
               job.bootstrap_file.bootstrap_state_file_path, job_id, broker_names, job_id, job_id,
               job_id, job_id, job_id),
    ]

    k_config["metadata"]["name"] = "bunnie-simulation-" + str(job_id)

    for broker in job.brokers:
      k_config["spec"]["template"]["spec"]["containers"].append({
          "name":
          "broker-" + broker.name.lower(),
          "image":
          broker.docker_image
      })

    try:
      resp = self._kubernetes_batch_v1_api.create_namespaced_job(body=k_config, namespace="default")
    except kubernetes.client.rest.ApiException as exception:
      self.update_job_status(job_id, simulation_job_pb2.SimulationJob.STATUS_READY)
      raise exception
