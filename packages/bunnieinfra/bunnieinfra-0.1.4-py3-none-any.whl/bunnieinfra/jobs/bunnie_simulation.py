# Kubernetes configuration template to run a simulation job. This template is used in
# ScheduleJobUtil.
_BUNNIE_SIMULATION_TEMPLATE = """
apiVersion: batch/v1
kind: Job

# The name of the job will be overriden in ScheduleJobUtil
metadata:
  name: bunnie-simulation

spec:
  template:
    spec:

      containers:
      - name: server-distribution
        image: andyccs/powertac-serverdistribution
        workingDir: '/usr/src/mymaven'

        command: ['/bin/sh']
        # More arguments are specified in ScheduleJobUtil

        # Security context is required to mount a volumne using gcsfuse command
        securityContext:
          privileged: True
          capabilities:
            add: ['SYS_ADMIN']

      restartPolicy: Never
"""
