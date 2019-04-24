# -*- coding: utf-8 -*-
from .base import XmlServiceTransport

__all__ = [
    'DatabaseTransport'
]


class DatabaseTransport(XmlServiceTransport):
    """Call XMLSERVICE using a database connection

    Args:
      conn: An active database connection object (PEP-249)
      schema (str, optional): The XMLSERVICE stored procedure schema
        to use
      **kwargs: Base transport options. See `XmlServiceTransport`.
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

    def call(self, tk):
        cursor = self.conn.cursor()

        parms = (self.ipc, self.ctl, tk.xml_in())

        # call the procedure using the correct method for this
        # cursor type, which we ascertained in the constructor
        getattr(cursor, self.func)(cursor, self.query, parms)

        return "".join(row[0] for row in cursor).rstrip('\0')
