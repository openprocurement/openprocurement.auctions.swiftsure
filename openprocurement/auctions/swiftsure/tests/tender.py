# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.tender import (
    AuctionResourceTestMixin,
    DgfInsiderResourceTestMixin,
    ExtractCredentialsMixin

)
from openprocurement.auctions.core.tests.blanks.tender_blanks import (
    # AuctionTest
    simple_add_auction,
    # AuctionResourceTest
    patch_tender_jsonpatch,
    auction_features_invalid,
    auction_features,
    # AuctionProcessTest
    invalid_auction_conditions,
)

from openprocurement.auctions.swiftsure.models import (
    SwiftsureAuction
)
from openprocurement.auctions.swiftsure.tests.base import (
    test_auction_data, test_organization, test_documents,
    BaseWebTest, BaseAuctionWebTest
)
from openprocurement.auctions.swiftsure.tests.blanks.tender_blanks import (
    # AuctionTest
    create_role,
    edit_role,
    # AuctionResourceTest
    create_auction_invalid,
    create_auction_auctionPeriod,
    create_auction_generated,
    create_auction,
    create_auction_with_documents,
    create_auction_with_documents_invalid,
    # AuctionProcessTest
    one_valid_bid_auction,
    one_invalid_bid_auction_manual,
    one_invalid_bid_auction_automatic,
    first_bid_auction,
    suspended_auction,
)


class AuctionTest(BaseWebTest):
    auction = SwiftsureAuction
    initial_data = test_auction_data

    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class AuctionResourceTest(
        BaseWebTest,
        AuctionResourceTestMixin,
        DgfInsiderResourceTestMixin):
    initial_status = 'active.tendering'
    initial_data = test_auction_data
    initial_organization = test_organization

    test_create_auction_invalid = snitch(create_auction_invalid)
    test_create_auction_auctionPeriod = snitch(create_auction_auctionPeriod)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction = snitch(create_auction)
    test_auction_features_invalid = unittest.skip(
        "option not available")(snitch(auction_features_invalid))
    test_auction_features = unittest.skip(
        "option not available")(snitch(auction_features))
    test_patch_tender_jsonpatch = snitch(patch_tender_jsonpatch)


class AuctionResourceTestWDocument(BaseWebTest):
    initial_status = 'active.tendering'
    initial_data = deepcopy(test_auction_data)
    documents = deepcopy(test_documents)
    initial_data['documents'] = documents

    test_create_auction_with_documents = snitch(create_auction_with_documents)
    test_create_auction_with_documents_invalid = snitch(
        create_auction_with_documents_invalid)


class AuctionProcessTest(BaseAuctionWebTest):
    test_financial_organization = None

    def setUp(self):
        super(AuctionProcessTest.__bases__[0], self).setUp()

    def change_ownership(self, auction_id, used_transfer_token):

        response = self.app.post_json('/transfers', {"data": {}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')

        transfer = response.json

        req_data = {"data": {"id": transfer['data']['id'],
                             'transfer': used_transfer_token}}
        response = self.app.post_json(
            '/auctions/{}/ownership'.format(auction_id), req_data
        )
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['data']['owner'], self.app.authorization[1][0]
        )

        response = self.app.get('/transfers/{}'.format(transfer['data']['id']))
        self.assertIn('usedFor', response.json['data'])
        self.assertEqual(
            '/auctions/{}'.format(auction_id), response.json['data']['usedFor']
        )
        owner_token = transfer['access']['token']

        return owner_token

    test_invalid_auction_conditions = unittest.skip(
        "option not available")(snitch(invalid_auction_conditions))
    test_one_valid_bid_auction = snitch(one_valid_bid_auction)
    test_one_invalid_bid_auction_manual = snitch(
        one_invalid_bid_auction_manual)
    test_one_invalid_bid_auction_automatic = snitch(
        one_invalid_bid_auction_automatic)
    test_first_bid_auction = snitch(first_bid_auction)
    test_suspended_auction = snitch(suspended_auction)


class AuctionExtractCredentialsTest(BaseAuctionWebTest, ExtractCredentialsMixin):
    pass


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionTest))
    tests.addTest(unittest.makeSuite(AuctionResourceTest))
    tests.addTest(unittest.makeSuite(AuctionProcessTest))
    suite.addTest(unittest.makeSuite(AuctionExtractCredentialsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
