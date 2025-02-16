import re


class MountEntry:
    """
    Represents a mount entry (device file, mount point and file system type)
    """

    def __init__(self, dev, point, fstype, options):
        self.dev = dev
        self.point = point
        self.fstype = fstype
        self.options = options.split(",")

    def __str__(self):
        return "{} on {} type {} ({})".format(
            self.dev,
            self.point,
            self.fstype,
            ",".join(self.options),
        )


MOUNT_PATTERN = re.compile(r"(.+?)\s+on\s+(.+?)\s+type\s+(\S+)(?:\s+\((.+?)\))?")


def mount_table():
    """returns the system's current mount table (a list of
    :class:`MountEntry <plumbum.unixutils.MountEntry>` objects)"""
    from plumbum.cmd import mount

    table = []
    for line in mount().splitlines():
        m = MOUNT_PATTERN.match(line)
        if not m:
            continue
        table.append(MountEntry(*m.groups()))
    return table


def mounted(fs):
    """
    Indicates if a the given filesystem (device file or mount point) is currently mounted
    """
    return any(fs == entry.dev or fs == entry.point for entry in mount_table())
