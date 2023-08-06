#
# Martin Kolman <mkolman@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#


import unittest
from tests.baseclass import CommandTest


class F29_TestCase(CommandTest):
    def runTest(self):
        # basic parsing
        self.assert_parse('module --name=nodejs --stream=6')
        self.assert_parse('module --name=foo --stream=1337')
        # non integer stream ids should also be fine
        self.assert_parse('module --name=bar --stream=baz')

        # --stream is optional
        self.assert_parse_error('module')
        self.assert_parse('module --name=foo')

        # but name needs to be always present
        self.assert_parse_error('module --stream=bar')

        # the values must not be empty
        self.assert_parse_error('module foo --name=bar --stream=')
        self.assert_parse_error('module foo --name= --stream=baz')
        self.assert_parse_error('module foo --name= --stream=')
        self.assert_parse_error('module foo --name --stream')
        self.assert_parse_error('module foo --name')

        # the module command does not take any absolute arguments
        self.assert_parse_error('module foo')
        self.assert_parse_error('module foo --name=bar')
        self.assert_parse_error('module foo --name=bar --stream=baz')

        # unknown options are an error
        self.assert_parse_error('module --name=bar --stream=baz --uknown=stuff')
        self.assert_parse_error('module --name=bar --uknown=stuff')

if __name__ == "__main__":
    unittest.main()
