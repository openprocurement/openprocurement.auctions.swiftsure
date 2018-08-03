# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.question import AuctionQuestionResourceTestMixin
from openprocurement.auctions.core.tests.blanks.question_blanks import (
    # AuctionLotQuestionResourceTest
    create_auction_question_lot,
    patch_auction_question_lot
)

from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest, test_lots
)


class AuctionQuestionResourceTest(
        BaseAuctionWebTest,
        AuctionQuestionResourceTestMixin):
    pass


@unittest.skip("option not available")
class AuctionLotQuestionResourceTest(BaseAuctionWebTest):
    initial_lots = 2 * test_lots

    test_create_auction_question_lot = snitch(create_auction_question_lot)
    test_patch_auction_question_lot = snitch(patch_auction_question_lot)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionQuestionResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotQuestionResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
