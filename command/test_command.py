import os
import tarfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from command.log_chronicle import archive_logs, FILE_NAME

runner = CliRunner()

def test_successful_run():
    with runner.isolated_filesystem():

        file_name = Path('hello.txt')

        with open(file_name, 'w') as f:
            f.write('Hello World!')

        result = runner.invoke(archive_logs, ['.', '.'])

        assert result.exit_code == 0
        assert file_name.exists()
        assert Path(FILE_NAME).exists()
        assert Path(FILE_NAME).suffixes == ['.tar', '.gz']

        file_name.unlink()
        tar = tarfile.open(FILE_NAME, mode='r:gz')

        for member in tar.members:
            tar.extract(member)

        assert file_name.exists()


def test_successful_run_compress_files_to_relative_path():
    with runner.isolated_filesystem():

        file_names = (Path('hello.txt'), Path('hello2.txt'),)

        for file in file_names:
            file.write_text('aaa')
        os.mkdir('test')

        result = runner.invoke(archive_logs, [file_names[0].name, 'test'])

        assert result.exit_code == 0

        for file in file_names:
            file.unlink()

        tar = tarfile.open('test/' + FILE_NAME, mode='r:gz')

        for member in tar.members:
            tar.extract(member)

        assert file_names[0].exists()
        assert not file_names[1].exists()


def test_symlink():

    with runner.isolated_filesystem():

        file_name = Path('hello.txt')
        file_name.write_text('Chasing bags')
        symlink = Path('link-to-textfile')
        symlink.symlink_to(file_name)

        result = runner.invoke(archive_logs, [symlink.name, '.'])

        assert result.exit_code == 0

        for file in (file_name, symlink):
            file.unlink()

        tar = tarfile.open(FILE_NAME, mode='r:gz')

        for member in tar.members:
            tar.extract(member)

        print(os.listdir('.'))
        assert file_name.exists()


def test_exception_destination_is_file():
    with runner.isolated_filesystem():
        result = runner.invoke(archive_logs, ['test'])
        assert type(result.exception) is ValueError

