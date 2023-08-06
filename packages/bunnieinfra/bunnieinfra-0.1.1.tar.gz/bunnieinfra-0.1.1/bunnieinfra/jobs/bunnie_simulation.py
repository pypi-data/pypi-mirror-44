_BUNNIE_SIMULATION_TEMPLATE = """
apiVersion: batch/v1
kind: Job
metadata:
  name: bunnie-simulation
spec:
  template:
    spec:

      # This volume is used to store the command to run server-distribution.
      volumes:
      - name: command-file
        emptyDir: {}

      # The init container creates main.sh, which is used to run server distribution.
      initContainers:
      - name: job-watcher
        image: alpine
        volumeMounts:
        - name: command-file
          mountPath: /usr/src/command-file/
        args: [
          '/bin/sh', '-c',
          'touch /usr/src/command-file/main.sh &&
           chmod 777 /usr/src/command-file/main.sh &&
           echo "mvn -Pcli -Dexec.args=\\"--sim --boot-data=bunnie-boot.xml --brokers=Bunnie\\"" > /usr/src/command-file/main.sh'
        ]

      containers:
      - name: server-distribution
        image: andyccs/powertac-serverdistribution
        volumeMounts:
        - name: command-file
          mountPath: /usr/src/mymaven/command-file/
        workingDir: '/usr/src/mymaven'
        command: ['/bin/sh']
        args: ['-c', '/usr/src/mymaven/command-file/main.sh']
        securityContext:
          privileged: True
          capabilities:
            add: ['SYS_ADMIN']

      restartPolicy: Never
"""
