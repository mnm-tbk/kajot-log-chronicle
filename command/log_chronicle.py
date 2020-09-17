import os
import shutil
import tarfile
from datetime import date
from typing import Optional, Tuple, IO, Type, TextIO

import click
from pathlib import Path

SOURCE = '/var/log'

DESTINATION = '/var/backup'

FILE_NAME = f'logs_{date.today()}.tar.gz'


def prepare_symlink(symlink: Path) -> Tuple[tarfile.TarInfo, TextIO]:
    return tarfile.TarInfo(Path(os.readlink(symlink)).name), open(Path(os.readlink(symlink)).resolve()),


@click.command()
@click.argument('source',
                default=SOURCE)
@click.argument('destination',
                default=DESTINATION)
@click.argument('file_name',
                default=FILE_NAME)
@click.option('--verbose', is_flag=True)
def archive_logs(source: Optional[str], destination: Optional[str], file_name: Optional[str],  verbose: bool):
    """ CLI interface for rotating logs in specified source folder.

    files and folders in source path will be compressed using gzip and saved to destination folder.

    --------------------- \n
    Defaults:  \n

    SOURCE = /var/log \n

    DESTINATION = /var/backups \n

    FILE_NAME = logs_{date.today()}.tar.gz \n

    --------------------- \n
    Usage:  \n
    >>> python archive_logs
      \n
    >>> python archive_logs --verbose
       \n
    >>> python archive_logs relative/path
       \n
    >>> python archive_logs /absolute/path
       \n
    >>> python archive_logs /absolute/path logs_from_prod
    """

    _source = Path(source)
    _file_name = Path(file_name)
    if _file_name.suffixes != ['.tar', '.gz'] and _file_name.suffixes != ['.tgz']:
        _file_name = Path(file_name + '.tar.gz')
    _cd = Path(destination)
    _destination = _cd / (Path(_file_name.name))

    if not _source.exists():
        raise ValueError('non existing path')

    if _destination.parent.is_file():
        raise TypeError('destination is a file')

    while _destination.exists():
        _file_name = Path('duplicate_' + _file_name.name)
        _destination = _cd / _file_name

    with tarfile.open(_destination, mode='w:gz', compresslevel=9, dereference=True) as f_out:
        if _source.is_file():
            if verbose:
                click.echo(f'+ {_source.name}')

            if _source.is_symlink():
                # noinspection PyTypeChecker
                f_out.addfile(*prepare_symlink(_source))
                return

            f_out.add(_source)
            return

        for file in _source.glob('*'):
            if file.name != _file_name:
                if verbose:
                    click.echo(f'+ {file.name}')

                if file.is_symlink():
                    # noinspection PyTypeChecker
                    f_out.addfile(*prepare_symlink(file))
                    continue

                f_out.add(file)

    if verbose:
        click.echo(f'\n Finished compression. Final archive has been saved to {_destination}')
        click.echo(f'\t Compressed size in MB: {_destination.stat().st_size / pow(2, 20)}')


if __name__ == '__main__':
    archive_logs()
