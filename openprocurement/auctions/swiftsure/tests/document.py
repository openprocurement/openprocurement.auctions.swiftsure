# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.swiftsure.tests.blanks.document_blanks import patch_auction_document


class AuctionDocumentResourceTest(BaseAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False
    test_patch_auction_document = snitch(patch_auction_document)


class AuctionDocumentWithDSResourceTest(BaseAuctionWebTest, AuctionDocumentResourceTestMixin, AuctionDocumentWithDSResourceTestMixin):
    docservice = True
    test_patch_auction_document = snitch(patch_auction_document)
    test_put_auction_document_pas = None
    test_create_auction_document_pas = None

    # TODO this TestCase didn't contain "test_create_auction_document_pas"


class AuctionDocumentResourceTestWithRegistry(AuctionDocumentResourceTest):
    registry = True
    test_patch_auction_document = snitch(patch_auction_document)


class AuctionDocumentWithDSResourceTestWithRegistry(AuctionDocumentWithDSResourceTest):
    registry = True
    test_patch_auction_document = snitch(patch_auction_document)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
