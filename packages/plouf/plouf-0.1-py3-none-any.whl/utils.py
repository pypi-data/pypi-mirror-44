import os
import click

# new dict class that we use with format_map,
# not throwing an error with a missing key found
class Default(dict):
    def __missing__(self, key):
        return key

def get_cwd():
    return os.getcwd()

def get_dirname():
    return os.path.basename(get_cwd())

def get_file_path(filename):
    cwd = get_cwd()
    return os.path.join(cwd, filename)

def file_exists(filename):
    f = get_file_path(filename)
    return os.path.exists(f)

def mkdirp(dirs):
    if not isinstance(dirs, list):
        mkdirp([dirs])
    else:
        for d in dirs:
            os.makedirs(d, exist_ok=True)

def list_files(startpath):
    for root, _, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        click.echo('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            click.echo('{}{}'.format(subindent, f))

# logger

def log(message, prefix, color, **kwargs):
    click.echo(
        click.style('[%s] ' % prefix.upper(), fg=color) + message,
        **kwargs
    )

def error(message, **kwargs):
    log(message, 'failure', 'red', **kwargs)

def warning(message, **kwargs):
    log(message, 'warning', 'yellow', **kwargs)

def info(message, **kwargs):
    log(message, 'info', 'blue', **kwargs)

def success(message, **kwargs):
    log(message, 'success', 'green', **kwargs)

