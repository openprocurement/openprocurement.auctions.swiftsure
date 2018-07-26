# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.bidder import (
    AuctionBidderDocumentResourceTestMixin,
    AuctionBidderDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.bidder_blanks import (
    # AuctionBidderFeaturesResourceTest
    features_bidder_invalid,
    # AuctionBidderResourceTest
    create_auction_bidder
)
from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest, test_features_auction_data,
)
from openprocurement.auctions.swiftsure.tests.blanks.bidder_blanks import (
    # AuctionBidderResourceTest
    create_auction_bidder_invalid,
    patch_auction_bidder,
    get_auction_bidder,
    delete_auction_bidder,
    get_auction_auctioners,
    bid_administrator_change,
    # AuctionBidderFeaturesResourceTest
    features_bidder,
    # AuctionBidderDocumentResourceTest
    create_auction_bidder_document_nopending,
    patch_auction_bidder_document,
    # AuctionBidderDocumentWithDSResourceTest
    operate_bidder_document_json_invalid
)


class AuctionBidderResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'

    test_financial_organization = None
    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)
    test_patch_auction_bidder = snitch(patch_auction_bidder)
    test_get_auction_bidder = snitch(get_auction_bidder)
    test_delete_auction_bidder = snitch(delete_auction_bidder)
    test_get_auction_auctioners = snitch(get_auction_auctioners)
    test_bid_administrator_change = snitch(bid_administrator_change)


@unittest.skip("option not available")
class AuctionBidderFeaturesResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.tendering'

    test_features_bidder = snitch(features_bidder)
    test_features_bidder_invalid = snitch(features_bidder_invalid)


class AuctionBidderDocumentResourceTest(
        BaseAuctionWebTest,
        AuctionBidderDocumentResourceTestMixin):
    initial_status = 'active.tendering'
    test_patch_auction_bidder_document = snitch(patch_auction_bidder_document)

    def setUp(self):
        super(AuctionBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json(
            '/auctions/{}/bids'.format(
                self.auction_id), {
                'data': {
                    'tenderers': [
                        self.initial_organization], "value": {
                        "amount": 500}, 'qualified': True}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']

    test_create_auction_bidder_document_nopending = snitch(
        create_auction_bidder_document_nopending)


class AuctionBidderDocumentWithDSResourceTest(
        BaseAuctionWebTest,
        AuctionBidderDocumentResourceTestMixin,
        AuctionBidderDocumentWithDSResourceTestMixin):
    initial_status = 'active.tendering'
    docservice = True
    test_patch_auction_bidder_document = snitch(patch_auction_bidder_document)

    def setUp(self):
        super(AuctionBidderDocumentWithDSResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json(
            '/auctions/{}/bids'.format(
                self.auction_id), {
                'data': {
                    'tenderers': [
                        self.initial_organization], "value": {
                        "amount": 500}, 'qualified': True}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']

        test_operate_bidder_document_json_invalid = snitch(  # noqa
            operate_bidder_document_json_invalid)

    test_create_auction_bidder_document_nopending = snitch(
        create_auction_bidder_document_nopending)

    def test_operate_bidder_document_json_invalid(self):
        """
            Check impossibility of operating with document where
            documentType = auctionProtocol
        """
        # Test POST auctionProtocol document
        response = self.app.post_json(
            '/auctions/{}/bids/{}/documents'.format(
                self.auction_id,
                self.bid_id),
            {
                'data': {
                    'title': 'name.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                    'documentType': 'auctionProtocol'}},
            status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['errors'][0]["description"],
            ["Value must be one of ["
             "'commercialProposal', 'qualificationDocuments', "
             "'eligibilityDocuments', 'financialLicense']."])

        # Test PUT auctionProtocol document
        response = self.app.post_json(
            '/auctions/{}/bids/{}/documents'.format(
                self.auction_id,
                self.bid_id),
            {
                'data': {
                    'title': 'name.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.put_json(
            '/auctions/{}/bids/{}/documents/{}'.format(
                self.auction_id,
                self.bid_id,
                doc_id),
            {
                'data': {
                    'title': 'name.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                    'documentType': 'auctionProtocol'}},
            status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['errors'][0]["description"],
            ["Value must be one of ["
             "'commercialProposal', 'qualificationDocuments', "
             "'eligibilityDocuments', 'financialLicense']."])

        # Test PATCH auctionProtocol document
        response = self.app.patch_json(
            '/auctions/{}/bids/{}/documents/{}'.format(
                self.auction_id, self.bid_id, doc_id), {
                'data': {
                    'documentType': 'auctionProtocol'}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['errors'][0]["description"],
            ["Value must be one of ["
             "'commercialProposal', 'qualificationDocuments', "
             "'eligibilityDocuments', 'financialLicense']."])


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionBidderResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderFeaturesResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
