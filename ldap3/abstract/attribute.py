"""
"""

# Created on 2014.01.06
#
# Author: Giovanni Cannata
#
# Copyright 2013 - 2016 Giovanni Cannata
#
# This file is part of ldap3.
#
# ldap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ldap3 in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

from os import linesep

from .. import SEQUENCE_TYPES
from ..core.exceptions import LDAPAttributeError
from ..utils.repr import to_stdout_encoding


# noinspection PyUnresolvedReferences
class Attribute(object):
    """Attribute/values object, it includes the search result (after post_query transformation) of each attribute in an entry

    Attribute object is read only

    - values: contain the processed attribute values
    - raw_values': contain the unprocessed attribute values


    """

    def __init__(self, attr_def, entry, reader):
        self.__dict__['key'] = attr_def.key
        self.__dict__['definition'] = attr_def
        self.__dict__['values'] = []
        self.__dict__['raw_values'] = []
        self.__dict__['entry'] = entry
        self.__dict__['reader'] = reader

    def __repr__(self):
        if len(self.values) == 1:
            r = self.key + ': ' + to_stdout_encoding(self.values[0])
        elif len(self.values) > 1:
            r = self.key + ': ' + to_stdout_encoding(self.values[0])
            filler = ' ' * (len(self.key) + 6)
            for value in self.values[1:]:
                r += linesep + filler + to_stdout_encoding(value)
        else:
            r = self.key + ': ' + to_stdout_encoding('<no value>')

        return r

    def __str__(self):
        if len(self.values) == 1:
            return to_stdout_encoding(self.values[0])
        else:
            return to_stdout_encoding(self.values)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return self.values.__iter__()

    def __getitem__(self, item):
        return self.values[item]

    def __setattr__(self, item, value):
        raise LDAPAttributeError('attribute \'%s\' is read only, use add_value(), set_value() or delete_value()' % item)

    def __eq__(self, other):
        try:
            if self.value == other:
                return True
        except:
            return False

    def add_value(self, value):
        # new value for attribute to commit with a MODIFY_ADD
        if value is not None and not self.definition.validate(self.definition.name, value):
            raise LDAPAttributeError('value %s non valid for attribute \'%s\'' % (value, item))
        self.__dict__['values_to_add'] = value if isinstance(value, SEQUENCE_TYPES) else [value]

    def set_value(self, value):
        # new value for attribute to commit with a MODIFY_REPLACE, old values are deleted
        if value is not None and not self.definition.validate(self.definition.name, value):
            raise LDAPAttributeError('value %s non valid for attribute \'%s\'' % (value, item))
        self.__dict__['values_to_replace'] = value if isinstance(value, SEQUENCE_TYPES) else [value]

    def delete_value(self, value):
        # value for attribute to delete in commit with a MODIFY_DELETE
        if value is not None and not self.definition.validate(self.definition.name, value):
            raise LDAPAttributeError('value %s non valid for attribute \'%s\'' % (value, item))
        self.__dict__['values_to_delete'] = value if isinstance(value, SEQUENCE_TYPES) else [value]


    @property
    def value(self):
        """
        :return: The single value or a list of values of the attribute.
        """
        return self.__dict__['values'][0] if len(self.__dict__['values']) == 1 else self.__dict__['values']
