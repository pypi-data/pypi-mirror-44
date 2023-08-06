from ..helpers.helpers import remove_sha_prefix
from ..lib.config import Config
from .abstract import AbstractObject


class Service(AbstractObject):
    def __init__(self, docker_client, service):
        super().__init__(docker_client, service)
        self._latest_sha = None
        self._current_sha = None

    def get_image_name(self):
        return self.service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image'].split(":", 1)[0]

    def get_tag(self):
        tag = self.service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image'].split(":", 1)
        if len(tag) == 2:
            tag = tag[1]
            if ":" in tag and "@" in tag:
                tag = tag.split("@")[0]
            return tag
        return "latest"

    def get_sha(self):
        tag = self.service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image'].split(":", 1)
        if len(tag) == 2:
            tag = tag[1]
            sha = ""
            if ":" in tag and "@" in tag:
                sha = tag.split("@")[1]
            return remove_sha_prefix(sha)
        return ""  # Empty, force to update this service for next time

    @property
    def service(self):
        return self.object

    def get_current_id(self):
        return (self._current_sha or "")[:10]

    def get_latest_id(self):
        return (self._latest_sha or "")[:10]

    def is_replicated(self):
        return self.service.attrs.get("Spec", {}).get("Mode", {}).get("Replicated", {})

    def _reload_object(self):
        self.object = self.client.services.get(self.service.name)

    def start(self):
        replicas_label = self.labels.get("dockupdater._replicas")
        if replicas_label or self.is_replicated().get("Replicas") == 0:  # Scale up
            replicas = int(replicas_label) if replicas_label else 1
            self.logger.debug('Scaling up service %s to %s', self.object.name, replicas)

            self.service.scale(replicas)
            self._reload_object()
        else:  # Force update
            self.service.force_update()

    def stop(self):
        replicated = self.is_replicated()
        if replicated:
            self.logger.debug('Scaling down service %s to 0', self.object.name)

            self.service.scale(0)
            self._reload_object()

            labels = self.labels
            labels["dockupdater._replicas"] = str(replicated.get("Replicas"))

            self.service.update(labels=labels)
            self._reload_object()
        else:
            self.logger.warning("Stop service is only available on replicated mode, not in global mode. Skip it.")

    @property
    def labels(self):
        return self.service.attrs.get('Spec', dict()).get('Labels', dict())

    @property
    def stack_name(self):
        return self.labels.get("com.docker.stack.namespace")

    def load_new_config(self):
        self.config = Config.from_labels(self.config, self.labels)

    def has_new_version(self):
        self.load_new_config()

        current_image_name = self.get_image_name()
        current_tag = self.get_tag()

        self.logger.debug("%s:%s", current_image_name, current_tag)

        current_sha = self.get_sha()
        if not current_sha:
            self.logger.error('No image SHA for %s. Update it for next time', current_image_name)

        if self.config.latest:
            current_tag = "latest"

        try:
            latest_image = self._pull(f"{current_image_name}:{current_tag}")
        except ConnectionError:
            return False

        latest_sha = self._get_digest(latest_image)
        self._latest_sha = latest_sha
        self._current_sha = current_sha
        return current_sha != latest_sha

    def update(self):
        if not self._latest_sha:
            self.has_new_version()

        self.logger.info('%s will be updated', self.name)
        self.service.update(image=f"{self.get_image_name()}:{self.get_tag()}@sha256:{self._latest_sha}")

    def _get_digest(self, image):
        digest = image.attrs.get(
            "Descriptor", {},
        ).get("digest") or image.attrs.get(
            "RepoDigests",
        )[0].split('@')[1] or image.id

        return remove_sha_prefix(digest)
