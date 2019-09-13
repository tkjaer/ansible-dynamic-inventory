#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dynamic Ansible Inventory based on LibreNMS API access.
"""

import argparse
import requests
import json
import re


parser = argparse.ArgumentParser(description='Return LibreNMS devices as a dynamic Ansible inventory.')
parser.add_argument('--list', help="return a list of full inventory of hosts", action="store_true")
parser.add_argument('--host', help="return hostsvars for a single host")
args = parser.parse_args()


librenms_hostname = 'https://hostname.example'
librenms_auth_token = 'replace-with-token'

headers = {
        'X-Auth-Token': librenms_auth_token,
        }


def get_device_details(device):
    """
    Takes a device object and returns a dict with the relevant details.
    """

    _device_details = {
            'sysname': device['sysName'],
            'hardware': device['hardware'],
            'location': device['location'],
            'type': device['type'],
            'ansible_network_os': device['os'],
            }

    return(_device_details)


def return_single_host(hostname):
    """
    Return the host variables for a single host.
    """

    r = requests.get(librenms_hostname + '/api/v0/devices/' + hostname, headers=headers)
    devices = json.loads(r.text)
    device = devices['devices'][0]

    device_details = get_device_details(device)

    print(json.dumps(device_details))


def return_full_inventory():
    """
    Return a full ansible inventory.
    """

    r = requests.get(librenms_hostname + '/api/v0/devices', headers=headers)
    librenms_devices = json.loads(r.text)


    # Create the basic inventory structure.
    # - http://docs.ansible.com/ansible/devel/dev_guide/developing_inventory.html
    # Do not create the 'ungrouped' group unless we truly have ungrouped, as per this bug:
    # https://github.com/ansible/ansible/pull/45621
    ansible_inventory = {
             "_meta": {
                 "hostvars": {},
                 },
             "all": {
                 "children": []
                 },
             }

    for device in librenms_devices['devices']:
        # Get the device type, based on our internal Naming Scheme (asw, csw, dsw, etc.)
        # - https://librenms1.rootdom.dk/plugin/p=Namingscheme
        device_type = re.match("^([a-zA-Z]*).*", device['hostname']).group(1)

        # Handle devices not matching our Naming Scheme
        if device_type == '':
            device_type = 'ungrouped'

        # Create a group for the device type if we don't already have one
        try:
            if (ansible_inventory[device_type]):
                pass
        except KeyError:
            ansible_inventory[device_type] = {
                    'hosts': [],
                        'vars': {
                               'connection': 'network_cli',
                            }
                    }
            ansible_inventory['all']['children'].append(device_type)

        hostname = device['hostname']

        # Add the host to the relevant device group
        ansible_inventory[device_type]['hosts'].append(hostname)

        # Add the host details to the _meta.hostvars dict
        ansible_inventory['_meta']['hostvars'][hostname] = get_device_details(device)

    print(json.dumps(ansible_inventory))


if args.host:
    return_single_host(args.host)
elif args.list:
    return_full_inventory()
