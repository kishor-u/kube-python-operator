# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project     : kube-python-operator-watch
@date        : 2020-01-29
@author      : kishor unnirkishnan
@description : a kubernetes operator is a high-level description of a deployable application to be run in a kubernetes
               cluster. this is a tiny kubernetes operator written in python that will watch the deployments in a
               namespace and set default cpu and memory limits on every deployment that doesn't have them.
"""

# Importing required libraries.
from conf.config import Const
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException


def main():
    # Module will load kube config from '~/.kube/config'.
    config.load_kube_config()  # use config.load_incluster_config() to load a Kubernetes config from within a cluster.

    # Create an instance of the API class.
    kube_api_instance = client.AppsV1Api()

    # Create an instance of the watch class.
    w = watch.Watch()

    # Initialising constants
    namespace = Const.NAMESPACE
    timeout = Const.WATCH_TIMER
    count = Const.COUNT_EVENTS
    deployments = []

    # API to update the cpu and memory of deployment object.
    def update_deployment(kube_api_instance, deployment):
        deployment_update_status = kube_api_instance.patch_namespaced_deployment(
                                                name=deployment.metadata.name,
                                                namespace=namespace,
                                                body=deployment)
        for i in range(len(deployment_update_status.status.conditions)):
            print("Deployment", deployment.metadata.name,
                  "Status : ", deployment_update_status.status.conditions[i].message)
        print("Deployment updated------->>>>>\n")

    # Stream created to watch k8s deployments default timer : set to 120 seconds in config
    try:
        for event in w.stream(kube_api_instance.list_namespaced_deployment,
                              namespace, timeout_seconds=timeout, watch=True):
            print(event['type'], event['object'].metadata.name)

            # For every deployment added we get multiple MODIFIED notifications.
            # Hence we will store those deployments in the timeframe and call update when it ends.
            if(event['type'] == 'MODIFIED'):
                if event['object'].metadata.name not in deployments:
                    deployments.append(event['object'].metadata.name)
            count -= 1
            if not count: w.stop()
        print("Finished watching deployment stream ---->>")
    except ApiException as e:
        print("Error in fetching deployment in the specified timeframe : %s\n" % e)

    for deployment_name in deployments:
        print("Processing deployment : ", deployment_name)
        api_response = kube_api_instance.read_namespaced_deployment(deployment_name, namespace)
        curr_deployment_obj = api_response
        curr_deployment_obj_container_count = len(curr_deployment_obj.spec.template.spec.containers)
        print("Number of containers in current deployment", curr_deployment_obj_container_count)

        for j in range(curr_deployment_obj_container_count):
            curr_container_request = curr_deployment_obj.spec.template.spec.containers[j].resources.requests
            curr_container_limit = curr_deployment_obj.spec.template.spec.containers[j].resources.limits

            # Handles requests parameteres here
            if(curr_container_request is None):
                Const.REQUEST_BODY['cpu'] = Const.CPU
                Const.REQUEST_BODY['memory'] = Const.MEMORY
            else:
                for key, value in curr_container_request.items():
                    if(key == 'memory'): Const.REQUEST_BODY['memory'] = value
                    if(key == 'cpu'): Const.REQUEST_BODY['cpu'] = value

                if(Const.REQUEST_BODY['cpu'] == ''): Const.REQUEST_BODY['cpu'] = Const.CPU
                if(Const.REQUEST_BODY['memory'] == ''): Const.REQUEST_BODY['memory'] = Const.MEMORY

            # Handles limits parameters here
            if(curr_container_limit is None):
                Const.LIMIT_BODY['cpu'] = Const.CPUS_LIMIT
                Const.LIMIT_BODY['memory'] = Const.MEM_LIMIT
            else:
                for key, value in curr_container_limit.items():
                    if(key == 'memory'): Const.LIMIT_BODY['memory'] = value
                    if(key == 'cpu'): Const.LIMIT_BODY['cpu'] = value

                if(Const.LIMIT_BODY['cpu'] == ''): Const.LIMIT_BODY['cpu'] = Const.CPUS_LIMIT
                if(Const.LIMIT_BODY['memory'] == ''): Const.LIMIT_BODY['memory'] = Const.MEM_LIMIT

            # Call API to update deployments not having CPU and Memory specified
            curr_deployment_obj.spec.template.spec.containers[j].resources.requests = Const.REQUEST_BODY
            curr_deployment_obj.spec.template.spec.containers[j].resources.limits = Const.LIMIT_BODY
            update_deployment(kube_api_instance, curr_deployment_obj)


if __name__ == '__main__':
    main()
