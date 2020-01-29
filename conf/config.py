class Const:
    NAMESPACE = "default"  # Specify your namespace here
    PRETTY = "true"

    MEMORY = "200Mi"       # Amount of memory requested to provide to container pods.
    CPU = "250m"           # Amount of cpu to requested provide to container pods.
    CPUS_LIMIT = "400m"    # CPUs (limit) for the container nodes pods. spec.containers[].resources.limits.cpu.
    MEM_LIMIT = "450Mi"    # Memory (limit) for the container nodes pods. spec.containers[].resources.limits.memory.

    REQUEST_BODY = {"cpu": '',
                    "memory": ''}

    LIMIT_BODY = {"cpu": '',
                    "memory": ''}

    COUNT_EVENTS = 15      # Max number of events watch timer listens before forceful shut down.
    WATCH_TIMER = 120      # Max amount of time in seconds the watcher will streams the event.
