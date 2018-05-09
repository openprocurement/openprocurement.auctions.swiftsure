# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.constants import DGF_PLATFORM_LEGAL_DETAILS_FROM

from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest
)
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)


class AuctionDocumentResourceTest(BaseAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False
    dgf_platform_legal_details_from = DGF_PLATFORM_LEGAL_DETAILS_FROM


class AuctionDocumentWithDSResourceTest(BaseAuctionWebTest, AuctionDocumentResourceTestMixin, AuctionDocumentWithDSResourceTestMixin):
    docservice = True
    dgf_platform_legal_details_from = DGF_PLATFORM_LEGAL_DETAILS_FROM

    # TODO this TestCase didn't contain "test_create_auction_document_pas"


class AuctionDocumentResourceTestWithRegistry(AuctionDocumentResourceTest):
    registry = True


class AuctionDocumentWithDSResourceTestWithRegistry(AuctionDocumentWithDSResourceTest):
    registry = True


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
