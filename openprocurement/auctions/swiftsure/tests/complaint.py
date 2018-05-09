# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest, test_lots,
)
from openprocurement.auctions.core.tests.complaint import (
    AuctionComplaintResourceTestMixin,
    InsiderAuctionComplaintDocumentResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.complaint_blanks import (
    # AuctionLotAwardComplaintResourceTest
    create_auction_complaint_lot
)


@unittest.skip("option not available")
class AuctionLotAwardComplaintResourceTest(BaseAuctionWebTest):
    initial_lots = test_lots

    test_create_auction_complaint_lot = snitch(create_auction_complaint_lot)


class AuctionComplaintDocumentResourceTest(BaseAuctionWebTest, InsiderAuctionComplaintDocumentResourceTestMixin):

    def setUp(self):
        super(AuctionComplaintDocumentResourceTest, self).setUp()
        # Create complaint
        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.initial_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionLotAwardComplaintResourceTest))
    tests.addTest(unittest.makeSuite(AuctionComplaintDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionComplaintResourceTest))
    return tests


class AuctionComplaintResourceTest(BaseAuctionWebTest, AuctionComplaintResourceTestMixin):
    """Test Case for Auction Complaint resource"""


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
