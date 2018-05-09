# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.contract import (
    AuctionContractResourceTestMixin,
    AuctionContractDocumentResourceTestMixin,
    Auction2LotContractDocumentResourceTestMixin
)
from openprocurement.auctions.core.plugins.contracting.v3.tests.prolongation import (
    AuctionContractProlongationResourceTestMixin
)
from openprocurement.auctions.core.plugins.contracting.v3.tests.contract import (
    AuctionContractV3ResourceTestCaseMixin
)
from openprocurement.auctions.core.tests.blanks.contract_blanks import (
    # Auction2LotContractResourceTest
    patch_auction_contract_2_lots,
)
from openprocurement.auctions.swiftsure.tests import fixtures
from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest,
    test_bids,
    test_lots,
    test_financial_auction_data,
    test_financial_bids,
    test_financial_organization,
)


class AuctionContractResourceTest(
    BaseAuctionWebTest,
    AuctionContractResourceTestMixin,
    AuctionContractV3ResourceTestCaseMixin
):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractResourceTest, self).setUp()
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id


@unittest.skip("option not available")
class Auction2LotContractResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotContractResourceTest, self).setUp()
        # Create award
        fixtures.create_award(self)

    test_patch_auction_contract_2_lots = snitch(patch_auction_contract_2_lots)


class AuctionContractDocumentResourceTest(BaseAuctionWebTest, AuctionContractDocumentResourceTestMixin):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractDocumentResourceTest, self).setUp()
        # Create award
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id


@unittest.skip("option not available")
class Auction2LotContractDocumentResourceTest(
    BaseAuctionWebTest,
    Auction2LotContractDocumentResourceTestMixin
):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotContractDocumentResourceTest, self).setUp()
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id


class AuctionContractProlongationResourceTest(BaseAuctionWebTest, AuctionContractProlongationResourceTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractProlongationResourceTest, self).setUp()
        self.app.authorization = ('Basic', ('token', ''))
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id # use autocreated contract
        fixtures.create_prolongation(self, 'prolongation_id')
        fixtures.create_prolongation(self, 'prolongation2_id')
        fixtures.create_prolongation(self, 'prolongation3_id')


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionContractResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotContractResourceTest))
    tests.addTest(unittest.makeSuite(AuctionContractDocumentResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotContractDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
