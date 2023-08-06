import unittest

from bunnieinfra.jobs.job_util import _ENTITY_KIND, _FIELD_JOB_STATUS, _FIELD_SIMULATION_JOB
from bunnieinfra.jobs.job_util import SimulationJobUtil
from bunnieshared.testutils.datastore import FakeDataStoreClient
from proto import simulation_job_pb2


class SimulationJobUtilTest(unittest.TestCase):
  """Tests for DataLoggerService."""

  def setUp(self):
    self._datastore_client = FakeDataStoreClient()
    self._simulation_job_util = SimulationJobUtil(datastore_client=self._datastore_client)

  def test_create_job(self):
    broker_name = "Bunnie"
    broker_image = "andyccs/bunnie-broker"
    google_cloud_storage_bucket_name = "bunnie.appspot.com"
    bootstrap_file_path = "powertac2018_bootfiles/PowerTAC_2018_Finals_1.xml"

    bunnie_broker = simulation_job_pb2.SimulationJob.Broker()
    bunnie_broker.name = broker_name
    bunnie_broker.docker_image = broker_image

    self._simulation_job_util.create_job(
        brokers=[bunnie_broker],
        google_cloud_storage_bucket_name=google_cloud_storage_bucket_name,
        bootstrap_file_path=bootstrap_file_path)

    entity = self._datastore_client.entity
    self.assertEqual(entity.key.entity_name[0], _ENTITY_KIND)
    self.assertEqual(entity[_FIELD_JOB_STATUS], simulation_job_pb2.SimulationJob.STATUS_READY)

    job = simulation_job_pb2.SimulationJob()
    job.MergeFromString(entity[_FIELD_SIMULATION_JOB])
    self.assertEqual(job.status, simulation_job_pb2.SimulationJob.STATUS_READY)
    self.assertEqual(len(job.brokers), 1)
    self.assertEqual(job.brokers[0].name, broker_name)
    self.assertEqual(job.brokers[0].docker_image, broker_image)
    self.assertEqual(job.bootstrap_file.google_cloud_storage_bucket_name,
                     google_cloud_storage_bucket_name)
    self.assertEqual(job.bootstrap_file.bootstrap_file_path, bootstrap_file_path)

  def test_create_job_datastore_error(self):
    bunnie_broker = simulation_job_pb2.SimulationJob.Broker()

    self._datastore_client.start_failing()
    with self.assertRaises(ValueError):
      self._simulation_job_util.create_job(
          brokers=[bunnie_broker],
          google_cloud_storage_bucket_name="bunnie.appspot.com",
          bootstrap_file_path="bootstrap_file.xml")

  def test_get_ready_job(self):
    entity = self._create_job()

    self._datastore_client.query_results = [entity]
    _, job = self._simulation_job_util.get_ready_job()
    self.assertEqual(job.status, simulation_job_pb2.SimulationJob.STATUS_READY)
    self.assertIsNone(self._datastore_client.entity)

  def test_get_ready_job_and_set_running(self):
    entity = self._create_job()

    self._datastore_client.query_results = [entity]
    _, job = self._simulation_job_util.get_ready_job(
        simulation_job_pb2.SimulationJob.STATUS_RUNNING)
    self.assertEqual(job.status, simulation_job_pb2.SimulationJob.STATUS_RUNNING)
    self.assertIsNotNone(self._datastore_client.entity)

  def test_get_ready_job_no_result(self):
    job_id, job = self._simulation_job_util.get_ready_job(
        simulation_job_pb2.SimulationJob.STATUS_RUNNING)
    self.assertIsNone(job_id)
    self.assertIsNone(job)

  def test_update_job_status(self):
    entity = self._create_job()
    self._datastore_client.get_result = entity

    self._simulation_job_util.update_job_status(
        simulation_job_id=1, new_job_status=simulation_job_pb2.SimulationJob.STATUS_RUNNING)

    entity = self._datastore_client.entity
    self.assertIsNotNone(entity)
    self.assertEqual(entity[_FIELD_JOB_STATUS], simulation_job_pb2.SimulationJob.STATUS_RUNNING)

    job = simulation_job_pb2.SimulationJob()
    job.MergeFromString(entity[_FIELD_SIMULATION_JOB])
    self.assertEqual(job.status, simulation_job_pb2.SimulationJob.STATUS_RUNNING)

  def _create_job(self):
    """Create a simulation job and return the job entity."""
    bunnie_broker = simulation_job_pb2.SimulationJob.Broker()
    bunnie_broker.name = "Bunnie"
    bunnie_broker.docker_image = "andyccs/bunnie-broker"

    self._simulation_job_util.create_job(
        brokers=[bunnie_broker],
        google_cloud_storage_bucket_name="bunnie.appspot.com",
        bootstrap_file_path="bootstrap_file.xml")
    entity = self._datastore_client.entity
    self._datastore_client.entity = None
    return entity


if __name__ == "__main__":
  unittest.main()
