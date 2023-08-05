import os
import json
import sys
import logging
import traceback

from pentagon.component import ComponentBase
from pentagon.component.aws_vpc import AWSVpc as Vpc
from pentagon.component.vpn import Vpn
from pentagon.component import gcp
from pentagon.helpers import create_rsa_key
from pentagon.defaults import AWSPentagonDefaults as PentagonDefaults


class Inventory(ComponentBase):

    _defaults = {'cloud': 'aws'}
    _required_parameters = [
        'name',
        'infrastructure_bucket',
        'aws_access_key',
        'aws_secret_key',
        'project_name'
    ]

    def __init__(self, data, additional_args=None, **kwargs):
        # HACK this if is to support start-project workflow
        if 'cloud' in data.keys():
            # HACK satisfy AWS requirements above in _required_parameters
            if data['cloud'] == 'gcp':
                data['aws_access_key'] = 'shouldneverbeused'
                data['aws_secret_key'] = 'shouldneverbeused'
        super(Inventory, self).__init__(data, additional_args, **kwargs)
        self._ssh_keys = {
            'admin_vpn_key': self._data.get('admin_vpn_key', PentagonDefaults.ssh['admin_vpn_key']),
            'working_kube_key': self._data.get('working_kube_key', PentagonDefaults.ssh['working_kube_key']),
            'production_kube_key': self._data.get('production_kube_key', PentagonDefaults.ssh['production_kube_key']),
            'working_private_key': self._data.get('working_private_key', PentagonDefaults.ssh['working_private_key']),
            'production_private_key': self._data.get('production_private_key', PentagonDefaults.ssh['production_private_key']),
        }

    @property
    def _files_directory(self):
        return sys.modules[self.__module__].__path__[0] + "/files/common"

    def add(self, destination, overwrite=False):
        """Inventory version of Component.add Copies files and templates from <component>/files and templates the *.jinja files """
        if destination == './':
            self._destination = self._data.get('name', './default')
        else:
            self._destination = destination

        self._overwrite = overwrite
        self._display_settings_to_user()

        try:
            self._add_files()

            if self._data['cloud'].lower() == 'aws':
                self._data['aws_region'] = self._data.get('aws_default_region')
                self._data['account'] = os.path.basename(self._destination)
                self._merge_data(self._ssh_keys)
                self.__create_keys()

                Aws(self._data).add("{}/terraform".format(self._destination))
                if self._data.get('configure_vpn', True):
                    Vpn(self._data).add(
                        "{}/resources".format(self._destination), overwrite=True)

            if self._data['cloud'].lower() == 'gcp':
                Gcp(self._data).add('{}/terraform/'.format(self._destination))

            self._remove_init_file()
            self._render_directory_templates()
        except Exception as e:
            logging.error("Error occurred configuring component")
            logging.error(e)
            logging.debug(traceback.format_exc(e))
            sys.exit(1)

    def __create_keys(self):
        key_path = "{}/{}/".format(self._destination, "config/private")

        for key in self._ssh_keys:
            logging.debug("Creating ssh key {}".format(key))
            key_name = "{}".format(self._ssh_keys[key])
            if not os.path.isfile("{}{}".format(key_path, key_name)):
                create_rsa_key(key_name, key_path)
            else:
                logging.warn("Key {}{} exist!".format(key_path, key_name))


class Aws(ComponentBase):

    def add(self, destination):
        Vpc(self._data).add("./{}".format(destination), overwrite=True)


class Gcp(ComponentBase):

    def add(self, destination):
        gcp.cluster.Public(self._data).add(
            "./{}".format(destination), overwrite=True)
