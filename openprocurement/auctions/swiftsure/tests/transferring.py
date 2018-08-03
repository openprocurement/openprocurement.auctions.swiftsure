# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.plugins.transferring.blanks.resource_blanks import (
    create_auction_by_concierge)
from openprocurement.auctions.core.tests.plugins.transferring.mixins import (
    AuctionOwnershipChangeTestCaseMixin
)
from openprocurement.auctions.swiftsure.tests.base import BaseAuctionWebTest


class AuctionOwnershipChangeResourceTest(BaseAuctionWebTest,
                                         AuctionOwnershipChangeTestCaseMixin):

    first_owner = 'broker3'
    second_owner = 'broker3'
    concierge = 'concierge'
    test_owner = 'broker3t'
    invalid_owner = 'broker1'
    initial_auth = ('Basic', (first_owner, ''))

    # swiftsure auction can not be changed during enquiryPeriod
    test_new_owner_can_change = None
    test_create_auction_by_concierge = snitch(create_auction_by_concierge)

    def setUp(self):
        super(AuctionOwnershipChangeResourceTest, self).setUp()
        self.not_used_transfer = self.create_transfer()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionOwnershipChangeResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
