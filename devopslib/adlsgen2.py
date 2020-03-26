import subprocess
import json
import logging

# Based on https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-directory-file-acl-cli

_file_system_name = None
_account_name = None

_log = logging.getLogger(__name__)

def connect_file_system(file_system_name=None, account_name=None):
    global _file_system_name, _account_name

    assert file_system_name or account_name, "at least one of file_system_name or account_name must be provided"
    if account_name:
        _account_name = account_name
        _log.debug(f"connect file_system_name={file_system_name}")
    if file_system_name:
        _file_system_name = file_system_name
        _log.debug(f"connect account_name={account_name}")
    

def is_dir(dir_name:str, file_system_name:str=None, account_name:str=None) -> bool:
    """Check if directory exists."""
    global _file_system_name, _account_name

    file_system_name = file_system_name or _file_system_name
    account_name = account_name or _account_name

    assert file_system_name, "file_system_name must be provided"
    assert account_name, "account_name must be provided"

    _log.debug(f"is_dir: {account_name}:{file_system_name}/{dir_name}")
    command = f'az storage blob directory exists -c "{file_system_name}" -d "{dir_name}" --account-name "{account_name}"'
    _log.debug(f"is_dir: command: {command}")
    process_result = subprocess.run(command, shell=True,
            capture_output=True)
    _log.debug(f"is_dir: returncode: {process_result.returncode}")
    _log.debug(f"is_dir: stdout: {process_result.stdout}")
    _log.debug(f"is_dir: stderr: {process_result.stderr}")
    if process_result.returncode != 0:
        raise Exception("Error: " + process_result.stderr.decode())
    result = json.loads(process_result.stdout)
    _log.debug("is_dir: " + str(result['exists']))
    return result['exists']


def create_dir(dir_name:str, file_system_name:str=None, account_name:str=None) -> bool:
    """Create directory."""
    global _file_system_name, _account_name

    file_system_name = file_system_name or _file_system_name
    account_name = account_name or _account_name

    assert file_system_name, "file_system_name must be provided"
    assert account_name, "account_name must be provided"

    command = f'az storage blob directory create -c "{file_system_name}" -d "{dir_name}" --account-name "{account_name}"'
    _log.debug(f"create_dir: executing: {command}")
    process_result = subprocess.run(command, shell=True,
            capture_output=True)
    _log.debug(f"create_dir: returncode: {process_result.returncode}")
    _log.debug(f"create_dir: stdout: {process_result.stdout}")
    _log.debug(f"create_dir: stderr: {process_result.stderr}")
    if process_result.returncode != 0:
        raise Exception("Error: " + process_result.stderr.decode())
    return json.loads(process_result.stdout)


def delete_dir(dir_name:str, file_system_name:str=None, account_name:str=None) -> bool:
    """Create directory."""
    global _file_system_name, _account_name

    file_system_name = file_system_name or _file_system_name
    account_name = account_name or _account_name

    assert file_system_name, "file_system_name must be provided"
    assert account_name, "account_name must be provided"

    command = f'az storage blob directory delete -c "{file_system_name}" -d "{dir_name}" --account-name "{account_name}"'
    _log.debug(f"delete_dir: executing: {command}")
    process_result = subprocess.run(command, shell=True,
            capture_output=True)
    _log.debug(f"delete_dir: returncode: {process_result.returncode}")
    _log.debug(f"delete_dir: stdout: {process_result.stdout}")
    _log.debug(f"delete_dir: stderr: {process_result.stderr}")
    if process_result.returncode != 0:
        raise Exception("Error: " + process_result.stderr.decode())
    return json.loads(process_result.stdout)

