__all__ = ['EnvFile', 'get', 'load']


import os
import values


def parse(line):
    """parse line and return a dictionary with variable value"""
    if line.lstrip().startswith('#'):
        return {}
    if not line.lstrip():
        return {}
    """find the second occurence of a quote mark:"""
    if line.find("export ") == 0:
        line = line.replace("export ", "", 1)
    quote_delimit = max(line.find('\'', line.find('\'') + 1),
                        line.find('"', line.rfind('"')) + 1)
    """find first comment mark after second quote mark"""
    if '#' in line:
        line = line[:line.find('#', quote_delimit)]
    key, value = map(lambda x: x.strip().strip('\'').strip('"'),
                     line.split('=', 1))
    return {key: value}


class EnvFile(dict):
    """.env file class"""
    path = None

    def __init__(self, path, **kwargs):
        self.path = os.path.abspath(os.path.expanduser(path))
        if os.path.exists(self.path):
            for line in open(self.path).read().splitlines():
                self.update(parse(line))
        for k, v in kwargs.items():
            self[k] = v

    def load(self):
        os.environ.update(self)

    def save(self):
        """save a dictionary to a file"""
        lines = []
        for key, value in self.items():
            lines.append("%s=%s" % (key, value))
        lines.append("")
        open(self.path, 'w').write("\n".join(lines))

    def __setitem__(self, key, value):
        super(EnvFile, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(EnvFile, self).__delitem__(key)


def get(path=".env"):
    """return a dictionary wit .env file variables"""
    if not path:
        path = ".env"
    data = dict()
    for path in values.get(path):
        if not os.path.exists(path):
            raise OSError("%s NOT EXISTS" % os.path.abspath(path))
        data.update(EnvFile(path))
    return data


def load(path=".env"):
    """set environment variables from .env file"""
    if not path:
        path = ".env"
    for path in values.get(path):
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(path):
            raise OSError("%s NOT EXISTS" % path)
        os.environ.update(get(path))
