from time import sleep

from docker.errors import APIError
from docker.errors import NotFound

from ..helpers.helpers import get_id_from_image
from ..helpers.helpers import remove_sha_prefix
from ..helpers.helpers import set_properties
from ..lib.config import Config
from .abstract import AbstractObject


class Container(AbstractObject):
    def __init__(self, docker_client, container):
        super().__init__(docker_client, container)
        self._latest_image = None
        self._current_id = None

    def get_image_name(self):
        return self.container.attrs['Config']['Image'].split(":", 1)[0]

    def get_tag(self):
        image = self.container.attrs['Config']['Image']
        if ":" in image:
            return image.split(":", 1)[1]
        else:
            tags = self.client.images.get(self.get_image_name()).tags
            if tags:
                tag = tags[0]
                if ":" in tag:
                    return tag.split(":", 1)[1]
                else:
                    return "latest"

    @property
    def container(self):
        return self.object

    @property
    def labels(self):
        return self.container.labels

    def get_current_id(self):
        return (self._current_id or "")[10:]

    def get_latest_id(self):
        if self._latest_image:
            return get_id_from_image(self._latest_image)[10:]
        return ""

    def is_dockupdater(self):
        dockupdater = "dockupdater" in self.container.attrs.get("Config", dict()).get("Image", self.name)
        if not dockupdater:
            for history in self.container.image.history():
                if "dockupdater" in (history.get("Tags", list()) or list()):
                    dockupdater = True
                    break
        if dockupdater:
            return True
        return False

    def load_new_config(self):
        self.config = Config.from_labels(self.config, self.container.labels)

    def has_new_version(self):
        self.load_new_config()

        current_image_name = self.get_image_name()
        current_tag = self.get_tag()
        self._current_id = remove_sha_prefix(self.container.attrs.get('Image', self.container.id))

        if self.config.latest:
            current_tag = "latest"

        try:
            latest_image = self._pull(f"{current_image_name}:{current_tag}")
            self._latest_image = latest_image
        except ConnectionError:
            return False

        latest_id = get_id_from_image(latest_image)

        return self._current_id != latest_id

    def update(self):
        if self.is_dockupdater():
            self.logger.info("Dockupdater container is ready to update")
            self.config.recreate_first = True  # Always recreate dockupdater container first
        elif self.container.attrs['Config'].get('ExposedPorts') and self.config.recreate_first:
            self.config.recreate_first = False
            self.logger.warning(
                "Option recreate_first isn't compatible when container has exposed ports. Option is set to False.",
            )

        if not self._current_id or not self._latest_image:
            self.has_new_version()

        if self.config.recreate_first:
            new_name = f"{self.name}_old"
            if self.is_dockupdater():
                new_name = f"{self.name}_old_dockupdater"
            self.container.rename(new_name)
        else:
            self.stop()
            self.remove()

        self.logger.info('%s will be updated', self.container.name)
        self.recreate()

        if self.is_dockupdater():
            self.logger.info('Waiting for new dockupdater container')
            sleep(600)

        if self.config.recreate_first:
            self.stop()
            self.remove()

        if self.config.cleanup:
            try:
                self.client.images.remove(self._current_id)
            except APIError as e:
                self.logger.error("Could not delete old image for %s, Error: %s", self.container.name, e)

    def start(self):
        self.logger.debug('Starting container: %s', self.object.name)
        self.container.start()

    def stop(self):
        self.logger.debug('Stopping container: %s', self.object.name)

        if self.config.stop_signal:
            try:
                self.container.kill(signal=self.config.stop_signal)
            except APIError as e:
                self.logger.error(
                    'Cannot kill container using signal %s. stopping normally. Error: %s',
                    self.object.stop_signal, e,
                )
                self.container.stop()
        else:
            self.container.stop()

    def remove(self):
        self.logger.debug('Removing container: %s', self.container.name)
        if not self.container.attrs.get('HostConfig', dict()).get('AutoRemove'):
            try:
                self.container.remove()
            except NotFound as e:
                self.logger.error("Could not remove container. Error: %s", e)
                return
        else:
            # Docker will remove container, but some time that take few seconds
            try:
                while True:
                    self.client.containers.get(self.name)
            except NotFound:
                pass

    def recreate(self):
        new_config = set_properties(
            old=self.container,
            new=self._latest_image,
            self_update=self.is_dockupdater(),
        )
        created = self.client.api.create_container(**new_config)
        new_container = self.client.containers.get(created.get("Id"))

        # connect the new container to all networks of the old container
        for network_name, network_config in self.container.attrs['NetworkSettings']['Networks'].items():
            network = self.client.networks.get(network_config['NetworkID'])
            try:
                network.disconnect(new_container.id, force=True)
            except APIError:
                pass
            new_network_config = {
                'container': new_container,
                'aliases': network_config['Aliases'],
                'links': network_config['Links'],
                'ipv4_address': network_config['IPAddress'],
                'ipv6_address': network_config['GlobalIPv6Address'],
            }
            try:
                network.connect(**new_network_config)
            except APIError as e:
                if any(err in str(e) for err in ['user configured subnets', 'user defined networks']):
                    if new_network_config.get('ipv4_address'):
                        del new_network_config['ipv4_address']
                    if new_network_config.get('ipv6_address'):
                        del new_network_config['ipv6_address']
                    network.connect(**new_network_config)
                else:
                    self.logger.error('Unable to attach updated container to network "%s". Error: %s', network.name, e)

        new_container.start()
