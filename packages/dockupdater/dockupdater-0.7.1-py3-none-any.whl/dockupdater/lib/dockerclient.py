from logging import getLogger
from os.path import isdir
from os.path import isfile
from os.path import join

from docker import DockerClient
from docker import tls


class Docker(object):
    """Class use to connect to the docker socket"""

    def __init__(self, socket, config, notification_manager):
        self.config = config
        self.socket = socket
        self.client = self.connect()
        self.logger = getLogger()

        self.notification_manager = notification_manager

    def connect(self):
        if self.config.docker_tls:
            try:
                cert_paths = {
                    'cert_top_dir': '/etc/docker/certs.d/',
                    'clean_socket': self.socket.split('//')[1],
                }
                cert_paths['cert_dir'] = join(cert_paths['cert_top_dir'], cert_paths['clean_socket'])
                cert_paths['cert_files'] = {
                    'client_cert': join(cert_paths['cert_dir'], 'client.cert'),
                    'client_key': join(cert_paths['cert_dir'], 'client.key'),
                    'ca_crt': join(cert_paths['cert_dir'], 'ca.crt'),
                }

                if not isdir(cert_paths['cert_dir']):
                    self.logger.error('%s is not a valid cert folder', cert_paths['cert_dir'])
                    raise ValueError

                for cert_file in cert_paths['cert_files'].values():
                    if not isfile(cert_file):
                        self.logger.error('%s does not exist', cert_file)
                        raise ValueError

                tls_config = tls.TLSConfig(
                    ca_cert=cert_paths['cert_files']['ca_crt'],
                    verify=cert_paths['cert_files']['ca_crt'] if self.config.docker_tls_verify else False,
                    client_cert=(cert_paths['cert_files']['client_cert'], cert_paths['cert_files']['client_key']),
                )
                client = DockerClient(base_url=self.socket, tls=tls_config)
            except ValueError:
                self.logger.error('Invalid Docker TLS config for %s, reverting to unsecured', self.socket)
                client = DockerClient(base_url=self.socket)
        else:
            client = DockerClient(base_url=self.socket)

        return client

    def check_swarm_mode(self):
        try:
            if not self.client.swarm or not self.client.swarm.attrs:
                self.logger.info("Your aren't running in swarm mode, skip services check.")
                self.config.disable_services_check = True
        except Exception as e:
            error_str = str(e).lower()
            if "this node is not a swarm manager" in error_str:
                if "worker nodes" in error_str:
                    raise EnvironmentError(
                        "Your running on a swarm worker, it isn't working. You must add placement constraints. "
                        "See docs at https://github.com/dockupdater/dockupdater for help.",
                    )
                else:
                    self.logger.info("Your aren't running in swarm mode, skip services check.")
                    self.config.disable_services_check = True
            else:
                raise e

        if self.config.disable_containers_check and self.config.disable_services_check:
            raise AttributeError("Error you can't disable all monitoring (containers/services).")
