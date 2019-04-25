# -*- coding: utf-8 -*-
"""
XMLSERVICE ssh call (ssh job, often in QUSRWRK)

License:
  BSD (LICENSE)
  -- or --
  http://yips.idevcloud.com/wiki/index.php/XMLService/LicenseXMLService

Example:
    from itoolkit.transport import SshTransport
    import paramiko
    ssh = paramiko.SSHClient()
    # configure paramiko. Using only WarningPolicy() is not secure
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(host, username="linux", password="linux1")
    itransport = SshTransport(ssh)

Notes:
    1) Always uses XMLSERVICE shipped in the QXMLSERV library
    2) does not disconnect the given SSHClient object when finished

"""
from .base import XmlServiceTransport

__all__ = [
    'SshTransport'
]


class SshTransport(XmlServiceTransport):
    """
    Transport XMLSERVICE calls over SSH connection.

    Args:
        sshclient (paramiko.SSHClient): connected and authenticated connection

    Example:
        from itoolkit.transport import SshTransport
        import paramiko
        ssh = paramiko.SSHClient()
        # configure paramiko. Using only WarningPolicy() is not secure
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        ssh.connect(host, username="linux", password="linux1")
        itransport = SshTransport(ssh)

    Returns:
       (obj)
    """

    def __init__(self, sshclient=None):
        # TODO: allow connection to be materialized from IBM Cloud deployments
        if not hasattr(sshclient, "exec_command"):
            raise Exception("An instance of paramiko.SSHClient is required")
        self.conn = sshclient

    def call(self, tk):
        """Call xmlservice with accumulated input XML.

        Args:
            tk  - iToolkit object

        Returns:
            xml
        """
        command = "/QOpenSys/pkgs/bin/xmlservice-cli"
        stdin, stdout, stderr = self.conn.exec_command(command)
        xml_in = tk.xml_in()
        stdin.write(xml_in.encode())
        stdin.flush()
        stdin.channel.shutdown_write()

        # rather than doing all this loop-de-loop, we could instead just use
        # a single call to stdout.readlines(), but there is a remote
        # possibility that the process is hanging writing to a filled-up
        # stderr pipe. So, we read a little from both until we're all done
        err_out = b""
        xml_out = b""
        blockSize = 64  # arbitrary
        while not stderr.closed or not stdout.closed:
            if not stderr.closed:
                newData = stderr.read(blockSize)
            if not newData:
                stderr.close()  # reaching EOF doesn't implicitly close
            else:
                err_out += newData
            if not stdout.closed:
                newData = stdout.read(blockSize)
            if not newData:
                stdout.close()  # reaching EOF doesn't implicitly close
            else:
                xml_out += newData
        stdout.channel.close()
        stderr.channel.close()
        return xml_out
