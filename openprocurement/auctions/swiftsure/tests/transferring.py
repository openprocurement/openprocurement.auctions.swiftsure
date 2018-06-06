# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.swiftsure.tests.base import BaseAuctionWebTest
from openprocurement.auctions.core.tests.plugins.transferring.mixins import (
    AuctionOwnershipChangeTestCaseMixin
)


class AuctionOwnershipChangeResourceTest(BaseAuctionWebTest,
                                         AuctionOwnershipChangeTestCaseMixin):

    first_owner = 'broker3'
    second_owner = 'broker3'
    test_owner = 'broker1t'
    invalid_owner = 'broker1'
    initial_auth = ('Basic', (first_owner, ''))

    test_mode_test = None

    def setUp(self):
        super(AuctionOwnershipChangeResourceTest, self).setUp()
        self.not_used_transfer = self.create_transfer()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionOwnershipChangeResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
