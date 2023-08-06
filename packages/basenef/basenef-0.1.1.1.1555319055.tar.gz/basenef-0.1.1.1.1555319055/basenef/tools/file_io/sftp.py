import paramiko
from contextlib import contextmanager
import os
from basenef.config import pkey, PUBKEY_PATH, PRVKEY_PATH


def ssh_gen():
    import rsa
    if os.path.isfile(PUBKEY_PATH):
        return PUBKEY_PATH

    (pubkey, prvkey) = rsa.newkeys(1024)

    pub = pubkey.save_pkcs1()
    with open(PUBKEY_PATH, 'w') as pubfile:
        pubfile.write(pub)

    prv = prvkey.save_pkcs1()
    with open(PRVKEY_PATH, 'w') as prvfile:
        prvfile.write(prv)
    return PRVKEY_PATH


@contextmanager
def ssh_connect(hostname = '127.0.0.1', port = 22, user = 'nef', pkey = pkey):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = hostname, port = port, username = user, pkey = pkey)
        yield ssh
    except ValueError(f'Connect to {hostname}:{port} failed'):
        pass
    finally:
        ssh.close()


@contextmanager
def build_transport(hostname = '127.0.0.1', port = 22, user = 'nef', pkey = pkey):
    transport = paramiko.Transport((hostname, port))
    try:
        transport.connect(username = user, pkey = pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        yield sftp
    except ValueError(f'Build transport to {hostname}:{port} failed'):
        pass
    finally:
        transport.close()


def sftp_upload(local_path, remote_path, *, hostname = '127.0.0.1', port = 22, user = 'nef',
                pkey = pkey):
    with build_transport(hostname, port, user, pkey) as sftp:
        sftp.put(local_path, remote_path)
    return remote_path


def sftp_download(remote_path, local_path, *, hostname = '127.0.0.1', port = 22, user = 'nef',
                  pkey = pkey):
    with build_transport(hostname, port, user, pkey) as sftp:
        sftp.get(remote_path, local_path)
    return local_path
