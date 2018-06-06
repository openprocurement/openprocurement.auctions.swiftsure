# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.blanks.migration_blanks import migrate

from openprocurement.auctions.swiftsure.migration import (
    migrate_data, SCHEMA_VERSION, get_db_schema_version
)
from openprocurement.auctions.swiftsure.tests.base import (
    BaseWebTest
)


class MigrateTest(BaseWebTest):
    migrate_data = staticmethod(migrate_data)
    get_db_schema_version = staticmethod(get_db_schema_version)
    schema_version = SCHEMA_VERSION

    def setUp(self):
        super(MigrateTest, self).setUp()
        migrate_data(self.app.app.registry)

    test_migrate = snitch(migrate)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(MigrateTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
