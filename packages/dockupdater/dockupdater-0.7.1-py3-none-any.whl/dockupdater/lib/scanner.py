from time import sleep

from ..helpers.helpers import convert_to_boolean
from ..update.container import Container
from ..update.service import Service
from .config import DISABLE_LABEL
from .config import ENABLE_LABEL
from .config import OptionRegex
from .notifiers import TemplateMessage


class Scanner(object):
    def __init__(self, docker_client):
        self.docker = docker_client
        self.logger = self.docker.logger
        self.config = self.docker.config
        self.client = self.docker.client
        self.socket = self.docker.socket
        self.notification_manager = self.docker.notification_manager

    def get_containers(self, option_regex=None):
        """Return a filtered by name list of containers"""
        if option_regex:
            args = dict(all=True)
        else:
            args = dict(filters={'status': 'running'})
        return [
            container
            for container in self.client.containers.list(ignore_removed=True, **args)
            if not option_regex or option_regex.match(container.name)
        ]

    def get_services(self, option_regex=None):
        """Return a filtered by name list of services"""
        return [
            service
            for service in self.client.services.list()
            if not option_regex or option_regex.match(service.name)
        ]

    def get_all_services_containers(self, option_regex):
        all = []

        if not self.config.disable_containers_check:
            all.extend([Container(self.docker, container) for container in self.get_containers(option_regex)])

        if not self.config.disable_services_check:
            all.extend([Service(self.docker, service) for service in self.get_services(option_regex)])

        return all

    def _scan_containers(self):
        """Return filtered container objects list to update"""
        monitored_containers = []

        for container in self.get_containers():
            enable_label = convert_to_boolean(container.labels.get(ENABLE_LABEL, False))
            disable_label = convert_to_boolean(container.labels.get(DISABLE_LABEL, False))
            swarm = container.labels.get('com.docker.stack.namespace', False)
            if (not self.config.label or enable_label) and not disable_label and not swarm:
                monitored_containers.append(Container(self.docker, container))
            else:
                self.logger.debug("skip monitoring for %s", container.name)

        self.logger.info("total containers monitored: %s", len(monitored_containers))

        return monitored_containers

    def _scan_services(self):
        """Return filtered service objects list to update"""
        monitored_services = []

        for service in self.get_services():
            enable_label = convert_to_boolean(service.attrs['Spec']['Labels'].get(ENABLE_LABEL, False))
            disable_label = convert_to_boolean(service.attrs['Spec']['Labels'].get(DISABLE_LABEL, False))
            if (not self.config.label or enable_label) and not disable_label:
                monitored_services.append(Service(self.docker, service))

        self.logger.info("total services monitored: %s", len(monitored_services))

        return monitored_services

    def scan_monitored(self):
        """Return all object update if there are a new version"""
        monitored = []

        if not self.config.disable_containers_check:
            monitored.extend(self._scan_containers())

        if not self.config.disable_services_check:
            monitored.extend(self._scan_services())

        return monitored

    def stops_before_update(self, container_or_service):
        """Stop some containers/services before update"""
        self.logger.debug("Checking to stop containers/services")
        for stop in container_or_service.config.stops:
            stop.tokens = {"stack": container_or_service.stack_name}
            for container_or_service in self.get_all_services_containers(stop):
                self.logger.info(f"Stopping {container_or_service.name} before update")
                container_or_service.stop()

    def starts_after_update(self, container_or_service):
        """start some containers/services after update"""
        self.logger.debug("Checking to start containers/services")
        for start in container_or_service.config.starts:
            start.tokens = {"stack": container_or_service.stack_name}
            for container_or_service in self.get_all_services_containers(start):
                self.logger.info(f"Staring {container_or_service.name} after update")
                container_or_service.start()

    def update(self):
        """Get the list of object, check if update is available, update it"""
        monitored = self.scan_monitored()

        if not monitored:
            self.logger.info('No containers/services are running or monitored on %s', self.socket)
            return

        for container_or_service in monitored:
            self.logger.debug("checking object %s", container_or_service.name)

            if container_or_service.has_new_version():
                self.stops_before_update(container_or_service)

                self.logger.info('%s will be updated', container_or_service.name)
                container_or_service.update()
                self.logger.debug('%s is updated', container_or_service.name)

                self.notification_manager.send(
                    TemplateMessage(container_or_service),
                    container_or_service.config.notifiers,
                )

                if container_or_service.config.wait:
                    self.logger.info('Waiting %s before next update', container_or_service.config.wait)
                    sleep(container_or_service.config.wait)

                self.starts_after_update(container_or_service)
            else:
                self.logger.debug("no new version for %s", container_or_service.name)

    def self_update(self):
        """Check for Dockupdater update"""
        if not self.config.disable_containers_check:
            # Removing old dockupdater
            self.logger.debug('Looking for old dockupdater on %s', self.socket)
            for container in self.get_containers(OptionRegex(".*_old_dockupdater")):
                self.logger.debug('Stopping and deleting %s', container.name)
                container.stop()
                container.remove()
            # Fix dockupdater if they need exposed port
            for container in self.get_containers():
                if container.labels.get("dockupdater.updater_port"):
                    self.logger.info(
                        'Recreate dockupdater container with exposed ports',
                    )
                    Container(self.docker, container)
                    container.update()
