import re
from copy import deepcopy
from logging import getLogger
from os import environ
from pathlib import Path

from ..helpers.helpers import convert_to_boolean
from .logger import BlacklistFilter

OPTION_REGEX_PATTERN = r"^(?:weight:(?P<weight>\d+),)?(?P<regex>.*)$"
DEFAULT_REGEX_WEIGHT = 100

MINIMUM_INTERVAL = 30

ENABLE_LABEL = "dockupdater.enable"
DISABLE_LABEL = "dockupdater.disable"

LABELS_MAPPING = {
    "dockupdater.latest": "latest",
    "dockupdater.notifiers": "notifiers",
    "dockupdater.stop_signal": "stop_signal",
    "dockupdater.cleanup": "cleanup",
    "dockupdater.template_file": "template_file",
    "dockupdater.wait": "wait",
    "dockupdater.recreate_first": "recreate_first",
    "dockupdater.starts": "starts",
    "dockupdater.stops": "stops",
}


class DefaultConfig(object):
    """Default configuration"""
    hostname = environ.get('HOSTNAME')
    interval = 300
    cron = None
    docker_sockets = ['unix://var/run/docker.sock']
    docker_tls = False
    docker_tls_verify = True
    log_level = 'info'
    cleanup = False
    run_once = False
    label = False
    stop_signal = None
    disable_containers_check = False
    disable_services_check = False
    latest = False
    wait = 0
    recreate_first = False

    stops = []
    starts = []

    repo_user = None
    repo_pass = None

    notifiers = []
    skip_start_notif = False
    template_file = None


class OptionRegex(object):
    def __init__(self, pattern):
        """pattern may be in these format:
            - weight:Digit,regex_pattern
            - regex_pattern
        """
        match = re.fullmatch(OPTION_REGEX_PATTERN, pattern, re.IGNORECASE).groupdict()
        try:
            re.compile(match.get("regex"))  # Test the regex
            self.regex = match.get("regex")
        except re.error:
            raise AttributeError("Invalid regex {} for option start or stop.".format(match.get("regex")))
        self.weight = int(match.get("weight") or DEFAULT_REGEX_WEIGHT)
        self.tokens = None

    def match(self, name):
        regex = self.regex
        if self.tokens:
            for token, value in self.tokens.items():
                if token and value:
                    regex = regex.replace("{" + str(token) + "}", value)
        return bool(re.fullmatch(regex, name))

    def __repr__(self):
        return f"<Option {self.regex}[{self.weight}]>"


class Config(object):
    def __init__(self, **kwargs):
        super().__setattr__("options", kwargs)
        self.logger = getLogger()
        self.compute_args()
        self.filtered_strings = None

    @classmethod
    def from_labels(cls, config, labels):
        """Create a new config object from an existing config and a dict of docker labels"""
        options = deepcopy(config.options)

        if labels:
            for label, value in labels.items():
                if label in LABELS_MAPPING:
                    if label in ["dockupdater.notifiers"]:
                        options[LABELS_MAPPING[label]] = value.split(" ")
                    elif label in ["dockupdater.latest", "dockupdater.cleanup"]:
                        options[LABELS_MAPPING[label]] = convert_to_boolean(value)
                    elif label in ["dockupdater.wait"]:
                        options[LABELS_MAPPING[label]] = int(value)
                    elif label in ["dockupdater.stops", "dockupdater.starts"]:
                        options[LABELS_MAPPING[label]] = [OptionRegex(item) for item in value.split(" ")]
                    else:
                        options[LABELS_MAPPING[label]] = value
                    if label == "dockupdater.template_file":
                        # Reload template
                        options["template"] = Config.load_template(options.get('template_file'))
                elif label.startswith("dockupdater."):
                    config.logger.warning("Warning label %s doesn't exist", label)

        return cls(**options)

    def __setattr__(self, key, value):
        if key in self.options:
            self.options[key] = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, attr):
        try:
            return self.options[attr]
        except KeyError:
            raise AttributeError

    def config_blacklist(self):
        """Mask sensitive data from logs"""
        filtered_strings = [
            getattr(self, key.lower()) for key, value in self.options.items()
            if key.lower() in BlacklistFilter.blacklisted_keys
        ]
        # Clear None values
        self.filtered_strings = list(filter(None, filtered_strings))
        # take lists inside of list and append to list
        for index, value in enumerate(self.filtered_strings, 0):
            if isinstance(value, list) or isinstance(value, tuple):
                self.filtered_strings.extend(self.filtered_strings.pop(index))
                self.filtered_strings.insert(index, self.filtered_strings[-1:][0])
        # Filter out no string item
        self.filtered_strings = [item for item in self.filtered_strings if isinstance(item, str)]
        # Added matching for ports
        ports = [string.split(':')[0] for string in self.filtered_strings if ':' in string]
        self.filtered_strings.extend(ports)
        # Added matching for tcp sockets. ConnectionPool ignores the tcp://
        tcp_sockets = [string.split('//')[1] for string in self.filtered_strings if '//' in string]
        self.filtered_strings.extend(tcp_sockets)
        # Get JUST hostname from tcp//unix
        for socket in getattr(self, 'docker_sockets'):
            self.filtered_strings.append(socket.split('//')[1].split(':')[0])

        for handler in self.logger.handlers:
            handler.addFilter(BlacklistFilter(set(self.filtered_strings)))

    def compute_args(self):
        if self.repo_user and self.repo_pass:
            self.options['auth_json'] = {'Username': self.repo_user, 'Password': self.repo_pass}
        else:
            self.options['auth_json'] = None

        if self.disable_containers_check and self.disable_services_check:
            raise AttributeError("Error you can't disable all monitoring (containers/services).")

        # Config sanity checks
        if self.cron:
            if not isinstance(self.cron, list):
                cron_times = self.cron.strip().split(' ')
                if len(cron_times) != 5:
                    self.logger.critical("Cron must be in cron syntax. e.g. * * * * * (5 places).")
                    raise AttributeError("Invalid cron")
                else:
                    self.logger.info("Cron configuration is valid. Using Cron schedule %s", cron_times)
                    self.cron = cron_times
                    self.interval = None
        else:
            if self.interval < MINIMUM_INTERVAL:
                self.logger.warning('Minimum value for interval was 30 seconds.')
                self.interval = MINIMUM_INTERVAL

        # Convert parameters to regex object
        self.stops = [OptionRegex(stop) if not isinstance(stop, OptionRegex) else stop for stop in self.stops]
        self.stops.sort(key=lambda x: x.weight)
        self.starts = [OptionRegex(start) if not isinstance(start, OptionRegex) else start for start in self.starts]
        self.starts.sort(key=lambda x: x.weight)

        self.options['template'] = Config.load_template(self.template_file)

    @staticmethod
    def load_template(template_file):
        # Load default template file
        if not template_file:
            dir_path = Path().absolute()
            template_file = dir_path.joinpath("dockupdater/templates/notification.j2")

        if Path(template_file).exists():
            with open(template_file) as f:
                return f.read()
        else:
            raise AttributeError(f"Template file {template_file} not found")
