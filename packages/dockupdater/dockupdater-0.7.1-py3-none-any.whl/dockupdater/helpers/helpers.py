def set_properties(old, new, self_update=False):
    """Store object for spawning new container in place of the one with outdated image"""
    labels = old.attrs['Config']['Labels']
    ports = None if not old.attrs['Config'].get('ExposedPorts') else [
        (p.split('/')[0], p.split('/')[1]) for p in old.attrs['Config']['ExposedPorts'].keys()
    ]

    if self_update:
        if ports:
            labels["dockupdater.updater_port"] = ":".join(["{},{}".format(a, b) for a, b in ports])
            ports = None
        elif labels.get("dockupdater.updater_port"):
            ports = [(int(port.split(",")[0]), port.split(",")[1])
                     for port in labels.get("dockupdater.updater_port").split(":")]
            labels["dockupdater.updater_port"] = None
            del labels["dockupdater.updater_port"]

    properties = {
        'name': old.name,
        'hostname': old.attrs['Config']['Hostname'],
        'user': old.attrs['Config']['User'],
        'detach': True,
        'domainname': old.attrs['Config']['Domainname'],
        'tty': old.attrs['Config']['Tty'],
        'ports': ports,
        'volumes': None if not old.attrs['Config'].get('Volumes') else [
            v for v in old.attrs['Config']['Volumes'].keys()
        ],
        'working_dir': old.attrs['Config']['WorkingDir'],
        'image': new.tags[0],
        'command': old.attrs['Config']['Cmd'],
        'host_config': old.attrs['HostConfig'],
        'labels': labels,
        'entrypoint': old.attrs['Config']['Entrypoint'],
        'environment': old.attrs['Config']['Env'],
    }

    return properties


def remove_sha_prefix(digest):
    if digest.startswith("sha256:"):
        return digest[7:]
    return digest


def convert_to_boolean(value):
    return str(value).lower() in ["yes", "y", "true", "1"]


def get_id_from_image(image):
    return remove_sha_prefix(image.attrs.get('Image', image.attrs.get(id, image.id)))
