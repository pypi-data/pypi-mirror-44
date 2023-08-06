from datetime import datetime
from datetime import timedelta
from datetime import timezone
from time import sleep

import click
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ConnectionError

from . import BRANCH
from . import VERSION
from .lib.config import Config
from .lib.config import DefaultConfig
from .lib.dockerclient import Docker
from .lib.logger import DockupdaterLogger
from .lib.notifiers import NotificationManager
from .lib.notifiers import StartupMessage
from .lib.scanner import Scanner


def apscheduler_wait(scheduler):
    while scheduler.get_jobs():
        sleep(10)


@click.command()
@click.version_option(version=VERSION)
@click.option(
    "-d", "--docker-sockets", "docker_sockets", envvar="DOCKER_SOCKETS",
    default=DefaultConfig.docker_sockets, show_default=True, multiple=True,
    help='Socket for docker management. EXAMPLE: -d unix://var/run/docker.sock',
)
@click.option(
    "-t", "--docker-tls", "docker_tls", envvar="DOCKER_TLS",
    is_flag=True, default=DefaultConfig.docker_tls, show_default=True,
    help='Enable docker TLS. REQUIRES: docker cert mount',
)
@click.option(
    "-T", "--docker-tls-verify", "docker_tls_verify", envvar="DOCKER_TLS_VERIFY",
    is_flag=True, default=DefaultConfig.docker_tls_verify, show_default=True,
    help='Verify the CA Certificate mounted for TLS',
)
@click.option(
    "-i", "--interval", "interval", envvar="INTERVAL",
    type=int, default=DefaultConfig.interval, show_default=True,
    help='Interval in seconds between checking for updates',
)
@click.option(
    "-C", "--cron", "cron", envvar="CRON",
    default=DefaultConfig.cron,
    help='Cron formatted string for scheduling. EXAMPLE: "*/5 * * * *"',
)
@click.option(
    "-l", "--log-level", "log_level", envvar="LOG_LEVEL",
    type=click.Choice(['debug', 'info', 'warn', 'error', 'critical']), default=DefaultConfig.log_level,
    show_default=True, help='Set logging level',
)
@click.option(
    "-L", "--latest", "latest", envvar="LATEST",
    default=DefaultConfig.latest, show_default=True, is_flag=True,
    help='Pull the :latest tags and update all containers to it.',
)
@click.option(
    "-o", "--run-once", "run_once", envvar="RUN_ONCE",
    is_flag=True, default=DefaultConfig.run_once, show_default=True,
    help='Single run',
)
@click.option(
    "-N", "--notifiers", "notifiers", envvar="NOTIFIERS",
    default=DefaultConfig.notifiers, multiple=True,
    help='Apprise formatted notifiers\n'
         'EXAMPLE: -N discord://1234123412341234/jasdfasdfasdfasddfasdf '
         'mailto://user:pass@gmail.com',
)
@click.option(
    "--skip-start-notif", "skip_start_notif", envvar="SKIP_START_NOTIF",
    default=DefaultConfig.skip_start_notif, is_flag=True, show_default=True,
    help='Skip notification of dockupdater has started',
)
@click.option(
    "--template-file", "template_file", envvar="TEMPLATE_FILE",
    default=DefaultConfig.template_file, type=click.Path(),
    help='Use a custom template for notification',
)
@click.option(
    "-k", "--label", "label", envvar="LABEL",
    default=DefaultConfig.label, is_flag=True, show_default=True,
    help='Enable label monitoring for dockupdater instead of monitoring all containers/services',
)
@click.option(
    "-c", "--cleanup", "cleanup", envvar="CLEANUP",
    default=DefaultConfig.cleanup, is_flag=True, show_default=True,
    help='Remove old images after updating',
)
@click.option(
    "-r", "--repo-user", "repo_user", envvar="REPO_USER",
    default=DefaultConfig.repo_user,
    help='Private docker registry username\n'
         'EXAMPLE: foo@bar.baz',
)
@click.option(
    "-R", "--repo-pass", "repo_pass", envvar="REPO_PASS",
    default=DefaultConfig.repo_pass,
    help='Private docker registry password',
)
@click.option(
    "--stop-signal", "stop_signal", envvar="STOP_SIGNAL",
    type=int, default=DefaultConfig.stop_signal,
    help='Override the stop signal send to container',
)
@click.option(
    "--disable-services-check", "disable_services_check", envvar="DISABLE_SERVICES_CHECK",
    default=DefaultConfig.disable_services_check, is_flag=True, show_default=True,
    help='Disable services (swarm) check',
)
@click.option(
    "--disable-containers-check", "disable_containers_check", envvar="DISABLE_CONTAINERS_CHECK",
    default=DefaultConfig.disable_containers_check, is_flag=True, show_default=True,
    help='Disable standalone containers check',
)
@click.option(
    "--hostname", "hostname",
    default=DefaultConfig.hostname, envvar="HOSTNAME",
    help='Set hostname (for debugging only)',
)
@click.option(
    "-w", "--wait", "wait", envvar="WAIT",
    default=DefaultConfig.wait, type=click.INT,
    help='Define a time in seconds to wait after an update before updating any others containers/services.',
)
@click.option(
    "-F", "--recreate-first", "recreate_first", envvar="RECREATE_FIRST",
    default=DefaultConfig.recreate_first, type=click.INT,
    help='Create a new container before stopping the old container.',
)
@click.option(
    "-s", "--stop", "stops", envvar="STOPS",
    default=DefaultConfig.stops, multiple=True,
    help='Regex to match Containers/Services to stop before update. May have a weight, '
         'lower will be stop first, of omit the default weight is 100. Example: --stop "weight:999,hello.*"',
)
@click.option(
    "-S", "--start", "starts", envvar="STARTS",
    default=DefaultConfig.starts, multiple=True,
    help='Regex to match Containers/Services to start after update. May have a weight, '
         'lower will be start first, of omit the default weight is 100 Example: --start "weight:1,hello.*',
)
def cli(
    docker_sockets, docker_tls, docker_tls_verify, interval, cron, log_level, run_once, notifiers,
    skip_start_notif, label, cleanup, repo_user, repo_pass, stop_signal, disable_services_check,
    disable_containers_check, template_file, hostname, latest, wait, recreate_first,
    starts, stops,
):
    """Declare command line options"""

    # Create App logger
    log = DockupdaterLogger(level=log_level)
    log.logger.info('Version: %s-%s', VERSION, BRANCH)

    config = Config(
        docker_sockets=docker_sockets,
        docker_tls=docker_tls,
        docker_tls_verify=docker_tls_verify,
        interval=interval,
        cron=cron,
        log_level=log_level,
        run_once=run_once,
        notifiers=notifiers,
        skip_start_notif=skip_start_notif,
        label=label,
        cleanup=cleanup,
        repo_user=repo_user,
        repo_pass=repo_pass,
        stop_signal=stop_signal,
        disable_services_check=disable_services_check,
        disable_containers_check=disable_containers_check,
        template_file=template_file,
        hostname=hostname,
        latest=latest,
        wait=wait,
        recreate_first=recreate_first,
        starts=starts,
        stops=stops,
    )
    config.config_blacklist()  # Configure mask on logger

    log.logger.debug("dockupdater configuration: %s", config.options)

    notification_manager = NotificationManager(config)
    scheduler = BackgroundScheduler()
    scheduler.start()

    for socket in config.docker_sockets:
        try:
            docker = Docker(socket, config, notification_manager)
            scanner = Scanner(docker)

            # Always begin to check the self update
            scanner.self_update()
            # Check docker swarm mode is running on a manager
            docker.check_swarm_mode()

            if config.cron:
                scheduler.add_job(
                    scanner.update,
                    name=f'Cron container update for {socket}',
                    trigger='cron',
                    minute=config.cron[0],
                    hour=config.cron[1],
                    day=config.cron[2],
                    month=config.cron[3],
                    day_of_week=config.cron[4],
                    misfire_grace_time=20,
                )
            else:
                if config.run_once:
                    scheduler.add_job(scanner.update, name=f'Run Once container update for {socket}')
                else:
                    scheduler.add_job(
                        scanner.update,
                        name=f'Initial run interval container update for {socket}',
                    )
                    scheduler.add_job(
                        scanner.update,
                        name=f'Interval container update for {socket}',
                        trigger='interval', seconds=config.interval,
                        misfire_grace_time=20,
                    )
        except ConnectionError:
            log.logger.error("Could not connect to socket %s. Check your config", config.socket)

    if config.run_once:
        next_run = None
    elif config.cron:
        next_run = scheduler.get_jobs()[0].next_run_time
    else:
        now = datetime.now(timezone.utc).astimezone()
        next_run = (now + timedelta(0, config.interval)).strftime("%Y-%m-%d %H:%M:%S")

    if not config.skip_start_notif:
        notification_manager.send(StartupMessage(config.hostname, next_run=next_run), config.notifiers)

    apscheduler_wait(scheduler)
    scheduler.shutdown()


def main():
    cli()


if __name__ == "__main__":
    main()
