#!/usr/bin/env python
"""
Author: Kapil Arora
Github: @kapilarora
"""
from solidfire.factory import ElementFactory


class SFClient(object):

    def __init__(self, ip, username, password):

        self._ip = ip
        self._username = username
        self._password = password
        self._client = self.create_sf_client()

    def create_sf_client(self):

        return ElementFactory.create(self._ip, self._username, self._password)

    def get_accounts(self):
        print 'getting accounts'
        return self._client.list_accounts()

    def get_volume(self, vol_name):
        return self._client.list_volumes(volume_name=vol_name).volumes[0]

    def remove_volume_pair(self, vol_id):
        return self._client.remove_volume_pair(volume_id=vol_id)

    def modify_volume_access(self, volume_id, access_type):
        return self._client.modify_volume(volume_id, access_type)

