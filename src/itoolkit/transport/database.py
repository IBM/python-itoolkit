# -*- coding: utf-8 -*-
import logging

from .base import XmlServiceTransport

__all__ = [
    'DatabaseTransport'
]


class DatabaseTransport(XmlServiceTransport):
    r"""Call XMLSERVICE using a database connection

    Args:
      conn: An active database connection object (PEP-249)
      schema (str, optional): The XMLSERVICE stored procedure schema
        to use
      **kwargs: Base transport options. See `XmlServiceTransport`.
    Examples:
        Connecting to XMLSERVICE over ODBC with the default \*LOCAL DSN on
        IBM i.

        >>> from itoolkit.transport import DatabaseTransport
        >>> import pyodbc
        >>> transport = DatabaseTransport(pyodbc.connect('DSN=*LOCAL'))

        Connecting to XMLSERVICE with ibm_db_dbi on IBM i.

        >>> from itoolkit.transport import DatabaseTransport
        >>> import ibm_db_dbi
        >>> transport = DatabaseTransport(ibm_db_dbi.connect())
    """
    def __init__(self, conn, **kwargs):
        # TODO: When we drop Python 2 support, add `*, schema='QXMLSERV'`
        # to the function variables, to make schema a keyword-only argument
        # and remove this block of code
        if 'schema' in kwargs:
            schema = kwargs['schema']
            del kwargs['schema']
        else:
            schema = 'QXMLSERV'

        if not hasattr(conn, 'cursor'):
            raise ValueError(
                "conn must be a PEP-249 compliant connection object")

        if not isinstance(schema, str) and schema is not None:
            raise ValueError("schema must be a string or None")

        super(DatabaseTransport, self).__init__(**kwargs)

        self.conn = conn

        self.procedure = "iPLUGR512K"
        if schema:
            self.procedure = schema + "." + self.procedure

        # We could simplify to just using execute, since we don't care
        # about output parameters, but ibm_db throws weird errors when
        # calling procedures with `execute` :shrug:
        if hasattr(self.conn.cursor(), 'callproc'):
            self.query = self.procedure
            self.func = 'callproc'
        else:
            self.query = "call {}(?,?,?)".format(self.procedure)
            self.func = 'execute'

        self.trace_attrs.extend([
            ('proc', 'procedure')
        ])

    def _call(self, tk):
        cursor = self.conn.cursor()

        parms = (self.ipc, self.ctl, tk.xml_in())

        # call the procedure using the correct method for this
        # cursor type, which we ascertained in the constructor
        getattr(cursor, self.func)(self.query, parms)

        # Use fetchall since not all adapters support the PEP-249 cursor
        # iteration extension eg. JayDeBeApi
        return "".join(row[0] for row in cursor.fetchall()).rstrip('\0')

    def _close(self):
        try:
            self.conn.close()
        except RuntimeError:
            # JayDeBeApi can fail to close a connection with
            # jpype._core.JVMNotRunning: Java Virtual Machine is not running
            #
            # Doesn't seem to be anything reasonable to do but log the
            # exception and continue.
            logging.exception("Unexpected exception closing database connection")
