# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.auctions.core.utils import SANDBOX_MODE
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.auctions import (
    AuctionAuctionResourceTestMixin,
    AuctionLotAuctionResourceTestMixin,
    AuctionMultipleLotAuctionResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.auction_blanks import (
    submission_method_details_no_auction,
    submission_method_details_fast_forward,
    # AuctionSameValueAuctionResourceTest
    post_auction_auction_not_changed,
    post_auction_auction_reversed,
    # AuctionFeaturesAuctionResourceTest
    get_auction_features_auction,
)

from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest, test_bids, test_lots,
    test_organization, test_features_auction_data,
    test_auction_data
)

from openprocurement.auctions.swiftsure.tests.blanks.auction_blanks import (
    # AuctionAuctionResourceTest
    post_auction_auction,
    # AuctionBidInvalidationAuctionResourceTest
    post_auction_all_invalid_bids,
    post_auction_one_invalid_bid,
    post_auction_one_valid_bid,
    # AuctionLotAuctionResourceTest
    post_auction_auction_lot,
    # AuctionMultipleLotAuctionResourceTest
    post_auction_auction_2_lots,
)


class AuctionAuctionResourceTest(
        BaseAuctionWebTest,
        AuctionAuctionResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids

    test_post_auction_auction = snitch(post_auction_auction)


class AuctionBidInvalidationAuctionResourceTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [test_organization],
            "value": {
                "amount": (
                    initial_data['value']['amount'] +
                    initial_data['minimalStep']['amount'] /
                    2),
                "currency": "UAH",
                "valueAddedTaxIncluded": True},
            'qualified': True} for i in range(3)]

    test_post_auction_all_invalid_bids = snitch(post_auction_all_invalid_bids)
    test_post_auction_one_invalid_bid = snitch(post_auction_one_invalid_bid)
    test_post_auction_one_valid_bid = snitch(post_auction_one_valid_bid)


class AuctionSameValueAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True
        }
        for i in range(3)
    ]

    test_post_auction_auction_not_changed = snitch(
        post_auction_auction_not_changed)
    test_post_auction_auction_reversed = snitch(post_auction_auction_reversed)


@unittest.skip("option not available")
class AuctionLotAuctionResourceTest(
        BaseAuctionWebTest,
        AuctionLotAuctionResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    initial_lots = test_lots

    test_post_auction_auction_lot = snitch(post_auction_auction_lot)


@unittest.skip("option not available")
class AuctionMultipleLotAuctionResourceTest(
        BaseAuctionWebTest,
        AuctionMultipleLotAuctionResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    test_post_auction_auction_2_lots = snitch(post_auction_auction_2_lots)


@unittest.skip("option not available")
class AuctionFeaturesAuctionResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.auction'
    initial_bids = [
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.1,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True
        },
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.15,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 479,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        }
    ]

    test_get_auction_auction_features = snitch(get_auction_features_auction)


@unittest.skipUnless(SANDBOX_MODE, u"Only in SANDBOX_MODE")
class AuctionSubmissionMethodDetailsTest(BaseAuctionWebTest):
    initial_data = deepcopy(test_auction_data)
    initial_bids = test_bids
    initial_status = 'active.auction'

    test_submission_method_details_no_auction = snitch(
        submission_method_details_no_auction)
    test_submission_method_details_fast_forward = snitch(
        submission_method_details_fast_forward)


class AuctionAuctionResourceTestWithRegistry(AuctionAuctionResourceTest):
    registry = True


class AuctionBidInvalidationAuctionResourceTestWithRegistry(
        AuctionBidInvalidationAuctionResourceTest):
    registry = True


class AuctionSameValueAuctionResourceTestWithRegistry(
        AuctionSameValueAuctionResourceTest):
    registry = True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSameValueAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionFeaturesAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSubmissionMethodDetailsTest))
    suite.addTest(unittest.makeSuite(AuctionSubmissionMethodDetailsTest))

    suite.addTest(unittest.makeSuite(AuctionAuctionResourceTestWithRegistry))
    suite.addTest(unittest.makeSuite(
        AuctionBidInvalidationAuctionResourceTestWithRegistry))
    suite.addTest(unittest.makeSuite(
        AuctionSameValueAuctionResourceTestWithRegistry))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
