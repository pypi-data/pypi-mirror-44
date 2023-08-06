from abc import ABC
from datetime import datetime
from datetime import timezone
from logging import getLogger

import apprise
from jinja2 import BaseLoader
from jinja2 import Environment

from ..update.service import Service


class BaseMessage(ABC):
    """Abstract message to send with apprise"""

    def __init__(self, title, body):
        self.title = title
        self.body = body


class StartupMessage(BaseMessage):
    def __init__(self, hostname, next_run=None):
        now = datetime.now(timezone.utc).astimezone()
        title = f'dockupdater has started'
        body_fields = [
            f'Host: {hostname}',
            f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")}',
            f'Next Run: {next_run}',
        ]
        super().__init__(title, '\n'.join(body_fields))


class TemplateMessage(BaseMessage):
    """Load and parse message to send from template file"""

    def __init__(self, container_or_service):
        if isinstance(container_or_service, Service):
            title = f'dockupdater has updated services!'
        else:
            title = f'dockupdater has updated containers!'

        template = Environment(loader=BaseLoader).from_string(container_or_service.config.template)
        body = template.render(object=container_or_service)
        super().__init__(title, body)


class NotificationManager(object):
    def __init__(self, config):
        self.config = config
        self.logger = getLogger()

    def build_apprise(self, notifiers):
        asset = apprise.AppriseAsset()
        asset.app_id = "dockupdater"
        asset.app_desc = "dockupdater"
        asset.app_url = "https://github.com/dockupdater/dockupdater"
        asset.html_notify_map['info'] = '#5F87C6'

        apprise_obj = apprise.Apprise(asset=asset)

        for notifier in notifiers:
            if notifier:
                add = apprise_obj.add(notifier)
                if not add:
                    self.logger.error('Could not add notifier %s', notifier)

        return apprise_obj

    def send(self, message, notifiers):
        apprise = self.build_apprise(notifiers)

        if apprise.servers:
            apprise.notify(title=message.title, body=message.body)
