from abc import ABC
from abc import abstractmethod

from docker.errors import APIError


class AbstractObject(ABC):
    def __init__(self, docker_client, object):
        self.docker = docker_client
        self.logger = self.docker.logger
        self.config = self.docker.config
        self.client = self.docker.client
        self.socket = self.docker.socket

        self.object = object

    @property
    def name(self):
        return self.object.name

    @property
    @abstractmethod
    def labels(self):
        """Return a dict with labels"""

    @abstractmethod
    def get_image_name(self):
        """Get image name"""

    @abstractmethod
    def get_tag(self):
        """Get image tag"""

    @abstractmethod
    def load_new_config(self):
        """Load config with labels"""

    @abstractmethod
    def has_new_version(self):
        """Return true if there are a new version"""

    @abstractmethod
    def get_current_id(self):
        """Return the current id for notification"""

    @abstractmethod
    def get_latest_id(self):
        """Return the latest id for notification"""

    @abstractmethod
    def start(self):
        """Start the container or service"""

    @abstractmethod
    def stop(self):
        """Stop the container or service"""

    @property
    def stack_name(self):
        return None

    def _pull(self, name_with_tag):
        """Docker pull image tag"""
        self.logger.debug('Checking tag: %s', name_with_tag)
        try:
            if self.config.auth_json:
                self.client.login(self.config.auth_json.get("username"), self.config.auth_json.get("password"))

            # The authentification doesn't work with this call
            # See bugs https://github.com/docker/docker-py/issues/2225
            # return self.client.images.get_registry_data(tag)
            return self.client.images.pull(name_with_tag, auth_config=self.config.auth_json)
        except APIError as e:
            if '<html>' in str(e):
                self.logger.debug("Docker api issue. Ignoring")
                raise ConnectionError
            elif 'unauthorized' in str(e):
                raise ConnectionError
            elif 'Client.Timeout' in str(e):
                self.logger.critical(
                    "Couldn't find an image on docker.com for %s. Local Build?", name_with_tag,
                )
                raise ConnectionError
            elif ('pull access' or 'TLS handshake') in str(e):
                self.logger.critical("Couldn't pull. Skipping. Error: %s", e)
                raise ConnectionError
