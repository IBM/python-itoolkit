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

import socket

__all__ = [
    'SshTransport'
]


class SshTransport(XmlServiceTransport):
    """
    Transport XMLSERVICE calls over SSH connection.

    Args:
        sshclient (paramiko.SSHClient): connected and authenticated connection

    Example:
        >>> from itoolkit.transport import SshTransport
        >>> import paramiko
        >>> ssh = paramiko.SSHClient()
        >>> ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        >>> ssh.connect(host, username="user", password="pass")
        >>> transport = SshTransport(ssh)

    .. warning::

        Using WarningPolicy is shown only as an example and could lead to
        security issues. Please refer to the `set_missing_host_key_policy`_
        docs for more info on other policies that may be more appropriate.

    .. _set_missing_host_key_policy: http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.set_missing_host_key_policy

    Returns:
       (obj)
    """  # noqa: E501 See https://github.com/PyCQA/pycodestyle/issues/888

    def __init__(self, sshclient=None, **kwargs):
        # TODO: allow connection to be materialized from IBM Cloud deployments
        if not hasattr(sshclient, "exec_command"):
            raise Exception("An instance of paramiko.SSHClient is required")

        super(SshTransport, self).__init__(**kwargs)

        self.conn = sshclient

    def _call(self, tk):
        """Call xmlservice with accumulated input XML.

        Args:
            tk  - iToolkit object

        Returns:
            xml
        """
        command = "/QOpenSys/pkgs/bin/xmlservice-cli"
        stdin, stdout, stderr = self.conn.exec_command(command)
        channel = stdout.channel

        xml_in = tk.xml_in()
        stdin.write(xml_in.encode())
        stdin.close()
        channel.shutdown_write()

        # Disable blocking I/O
        # chan.settimeout(0.0) is equivalent to chan.setblocking(0)
        # https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.settimeout
        channel.settimeout(0.0)

        # rather than doing all this loop-de-loop, we could instead just use
        # a single call to stdout.readlines(), but there is a remote
        # possibility that the process is hanging writing to a filled-up
        # stderr pipe. So, we read from both until we're all done
        err_out = b""
        xml_out = b""

        # Convenience wrapper for reading data from stdout/stderr
        # Returns empty binary string if EOF *or* timeout (no data)
        # Closes file on EOF
        def read_data(f):
            if f.closed:
                return b""

            try:
                data = f.read()
                if not data:
                    f.close()
                return data
            except socket.timeout:
                return b""

        while not all((stdout.closed, stderr.closed)):
            xml_out += read_data(stdout)
            err_out += read_data(stderr)

        channel.close()
        return xml_out

    def _close(self):
        self.conn.close()
