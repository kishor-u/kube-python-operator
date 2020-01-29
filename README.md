## A Sample Kubernetes Operator

A Kubernetes operator is a high-level description of a deployable application to be run in a Kubernetes cluster. This is a tiny Kubernetes operator written in **Python** to set default cpu and memory limits on every deployment and statefulset that doesn't have them.

### How it Works

- The operator can be used in many ways.
1) Can be used as a static opertor to be run in the local machine where you make the kubectl commands.

2) Create the docker image of the operator (sample dockerfile provided) and a Kubernetes cronjob scheduled to run in a namespace at a specific time.


### How to Run

- Clone the repo to your system by `git clone https://github.com/kishorgec/kudo-python-operator.git`

- Make sure that you have the latest **kubectl** installed on the client machine. Kubectl is a command line tool for controlling Kubernetes clusters. kubectl looks for a file named config in the $HOME/.kube directory.

- Type commands
```
python deployment_operator.py    // for managing deployment objects in the namespace

python statefulset_operator.py   // for managing statefulset objects in the namespace
```
