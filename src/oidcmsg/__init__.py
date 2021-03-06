__author__ = 'Roland Hedberg'
__version__ = '1.1.2'

VERIFIED_CLAIM_PREFIX = '__verified'


def verified_claim_name(claim):
    return '{}_{}'.format(VERIFIED_CLAIM_PREFIX, claim)


def proper_path(path):
    """
    Clean up the path specification so it looks like something I could use.
    "./" <path> "/"
    """
    if path.startswith("./"):
        pass
    elif path.startswith("/"):
        path = ".%s" % path
    elif path.startswith("."):
        while path.startswith("."):
            path = path[1:]
        if path.startswith("/"):
            path = ".%s" % path
    else:
        path = "./%s" % path

    if not path.endswith("/"):
        path += "/"

    return path


# This is for adding a base path to path specified in a configuration
def add_base_path(conf, item_paths, base_path):
    for section, items in item_paths.items():
        if section == "":
            part = conf
        else:
            part = conf.get(section)

        if part:
            if isinstance(items, list):
                for attr in items:
                    _path = part.get(attr)
                    if _path:
                        if _path.startswith("/"):
                            continue
                        elif _path == "":
                            part[attr] = "./" + _path
                        else:
                            part[attr] = os.path.join(base_path, _path)
            elif items is None:
                if part.startswith("/"):
                    continue
                elif part == "":
                    conf[section] = "./"
                else:
                    conf[section] = os.path.join(base_path, part)
            else:  # Assume items is dictionary like
                add_base_path(part, items, base_path)
