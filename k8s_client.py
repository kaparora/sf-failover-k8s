#!/usr/bin/env python
"""
Author: Kapil Arora
Github: @kapilarora
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class K8SClient(object):

    def __init__(self, kubeconfig):

        self._kubeconfig = kubeconfig
        self._client = self.create_k8s_client()

    def create_k8s_client(self):
        config.load_kube_config(self._kubeconfig)
        return client.CoreV1Api()

    def get_all_pvs(self):
        return self._client.list_persistent_volume()

    def update_pv(self, pv_name, pv):
        return self._client.replace_persistent_volume(pv_name, pv)


