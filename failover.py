#!/usr/bin/env python
"""
Author: Kapil Arora
Github: @kapilarora
"""
from solidfire_client import SFClient
from k8s_client import K8SClient
from kubernetes.client.rest import ApiException
import os
from time import strftime
import logging

def main():

    k8s_config = os.environ['KUBECONFIG']
    ip = os.environ['SF_IP']
    username = os.environ['SF_USERNAME']
    password = os.environ['SF_PASSWORD']
    target_portal = os.environ['SF_TARGET_PORTAL']
    no_execute_str = os.environ['NO_EXECUTE']
    if no_execute_str.lower() == 'true':
        no_execute = True
    else:
        no_execute = False
    log_level_str = os.environ['LOG_LEVEL']
    log_level = _get_Log_level(log_level_str)

    log_filename = strftime("sf_failover_k8s_%Y%m%d%H%M%S.log")
    logging.basicConfig(filename=log_filename,
                        level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting the failover script with following options:')
    logging.info('KUBECONFIG: %s',k8s_config)
    logging.info('SF_IP: %s', ip)
    logging.info('SF_USERNAME: %s', username)
    logging.info('SF_PASSWORD: %s', password)
    logging.info('SF_TARGET_PORTAL: %s', target_portal)
    if no_execute:
        logging.info('This is just a dry run!')

    sf = SFClient(ip, username, password)

    k8s = K8SClient(k8s_config)
    pvs = k8s.get_all_pvs()

    logging.info('Getting IDs and IQNs for all iSCSI Volumes (PVCs) from SolidFire')
    vol_ids = {}
    vol_iqns= {}

    for pv in pvs.items:
        pv_name = pv.metadata.name
        logging.info('Processing PV %s', pv_name)
        if pv.spec.iscsi is not None:
            logging.info('Verified PV %s is an iSCSI volume', pv_name)
            vol = sf.get_volume(pv_name)

            vol_id = vol.volume_id
            vol_ids[pv_name] = vol_id

            vol_iqn = vol.iqn
            vol_iqns[pv_name] = vol_iqn


    logging.info('Starting removal of all volume pairs')

    for pv_name in vol_ids:
        # remove volume pair
        vol_id = vol_ids[pv_name]
        if no_execute:
            logging.info('Not Removing volume pair for volume %s with vol id: %s as this is a dry run.',
                         pv_name, vol_id)
        else:
            logging.info('Removing volume pair for volume %s with vol id: %s', pv_name, vol_id)
            sf.remove_volume_pair(vol_id)
            logging.info('Remove Volume pair started', )

    logging.info('Starting changing all volume access to readWrite')
    for pv_name in vol_ids:
        vol_id = vol_ids[pv_name]
        # change volume access type
        if no_execute:
            logging.info(
                'Not Changing volume access type to readWrite for volume %s with vol id: %s as this is a dry run.',
                pv_name, vol_id)
        else:
            logging.info('Changing volume access type to readWrite for volume %s with vol id: %s .',
                         pv_name, vol_id)
            sf.modify_volume_access(vol_id, 'readWrite')
            logging.info('Modified volume accesstype to readWrite', )



    logging.info('Starting Updating PVs with  new IQN and target portal')
    for pv in pvs.items:
        pv_name = pv.metadata.name
        logging.info('Processing PV %s', pv_name)
        if pv.spec.iscsi is not None:
            logging.info('Verified PV %s is an iSCSI volume', pv_name)
            vol_iqn = vol_iqns[pv_name]

            #update pv
            logging.info('Changing iqn for PV from %s to %s', pv.spec.iscsi.iqn, vol_iqn)
            pv.spec.iscsi.iqn = vol_iqn
            logging.info('Changing target_portal for PV from %s to %s', pv.spec.iscsi.target_portal, target_portal)
            pv.spec.iscsi.target_portal = target_portal

            try:

                if no_execute:
                    logging.info('Not Updating PV %s as this a dry run', pv_name)
                else:
                    logging.info('Updating PV %s', pv_name)
                    pv_updated = k8s.update_pv(pv_name, pv)
                    logging.debug('Returned Updated PV %s', pv_updated)

            except ApiException as e:
                print("Exception when calling CoreV1Api->patch_persistent_volume: %s\n" % e)


def _get_Log_level(log_level):
    '''

    :param log_level: str info/error/warn/debug
    :return: logging.level
    '''
    if log_level == 'info':
        level = logging.INFO
    elif log_level == 'error':
        level = logging.ERROR
    elif log_level == 'warn':
        level = logging.WARN
    else:
        level = logging.DEBUG
    return level


if __name__ == '__main__':
    main()