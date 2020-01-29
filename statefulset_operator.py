# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project     : kube-python-operator
@date        : 2020-01-28
@author      : kishor unnirkishnan
@description : a kubernetes operator is a high-level description of a deployable application to be run in a kubernetes
               cluster. this is a tiny kubernetes operator written in python to set default cpu and memory limits on
               every statefulset that doesn't have them.
"""

# Importing required libraries.
from conf.config import Const
from kubernetes import config, client
from kubernetes.client.rest import ApiException


def main():
    # Module will load kube config from '~/.kube/config'.
    config.load_kube_config()  # use config.load_incluster_config() to load a Kubernetes config from within a cluster.

    # Create an instance of the API class.
    kube_api_instance = client.AppsV1Api()

    # Initialising constants
    namespace = Const.NAMESPACE
    pretty = Const.PRETTY

    # API to update the cpu and memory of statefulset object.
    def update_statefulset(kube_api_instance, statefulset):
        statefulset_update_status = kube_api_instance.patch_namespaced_stateful_set(
                                                name=statefulset.metadata.name,
                                                namespace=namespace,
                                                body=statefulset)
        print("Statefulset", statefulset.metadata.name,
              "updated to revision :", statefulset_update_status.status.update_revision)
        print("Statefulset updated------->>>>>\n")

    # API to fetch current statefulset
    try:
        curr_statefulsets = kube_api_instance.list_namespaced_stateful_set(namespace, pretty=pretty)
        curr_statefulset_count = len(curr_statefulsets.items)
        if curr_statefulset_count == 0:
            print("No statefulsets exists in the namespace provided")

        for i in range(curr_statefulset_count):
            curr_statefulset_obj = curr_statefulsets.items[i]
            print(curr_statefulset_obj.metadata.name)
            curr_statefulset_obj_container_count = len(curr_statefulset_obj.spec.template.spec.containers)
            print("Number of containers in current statefulset  ", curr_statefulset_obj_container_count)

            for j in range(curr_statefulset_obj_container_count):
                curr_container_request = curr_statefulset_obj.spec.template.spec.containers[j].resources.requests
                curr_container_limit = curr_statefulset_obj.spec.template.spec.containers[j].resources.limits

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

                # Call API to update statefulsets not having CPU and Memory specified
                curr_statefulset_obj.spec.template.spec.containers[j].resources.requests = Const.REQUEST_BODY
                curr_statefulset_obj.spec.template.spec.containers[j].resources.limits = Const.LIMIT_BODY
                update_statefulset(kube_api_instance, curr_statefulset_obj)

    except ApiException as e:
        print("Exception on API call : [listing stateful set] %s\n" % e)


if __name__ == '__main__':
    main()
