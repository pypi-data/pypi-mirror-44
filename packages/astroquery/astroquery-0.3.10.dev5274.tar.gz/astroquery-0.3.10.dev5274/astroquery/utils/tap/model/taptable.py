# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
=============
TAP plus
=============

@author: Juan Carlos Segovia
@contact: juan.carlos.segovia@sciops.esa.int

European Space Astronomy Centre (ESAC)
European Space Agency (ESA)

Created on 30 jun. 2016


"""


class TapTableMeta(object):
    """TAP table metadata object
    """

    def __init__(self):
        """Constructor
        """
        self.columns = []
        self.name = None
        self.schema = None
        self.description = None

    def get_qualified_name(self):
        """Returns the qualified TAP table name. I.e. schema+table

        Returns
        -------
        The the qualified TAP table name (schema+table)
        """
        return self.schema + "." + self.name

    def add_column(self, tap_column):
        """Adds a table TAP column

        Parameters
        ----------
        tap_column : TAP Column object, mandatory
            table TAP column
        """
        self.columns.append(tap_column)

    def __str__(self):
        return "TAP Table name: " + str(self.get_qualified_name()) + \
            "\nDescription: " + str(self.description) + \
            "\nNum. columns: " + str(len(self.columns))
