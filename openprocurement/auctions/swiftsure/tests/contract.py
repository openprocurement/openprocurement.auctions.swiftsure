# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.contract import (
    AuctionContractResourceTestMixin,
    AuctionContractDocumentResourceTestMixin,
    Auction2LotContractDocumentResourceTestMixin
)

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.plugins.contracting.v3_1.tests.contract import (
    AuctionContractV3_1ResourceTestCaseMixin)
from openprocurement.auctions.core.tests.plugins.contracting.v3_1.tests.blanks.contract_blanks import (
    # Auction2LotContractResourceTest
    patch_auction_contract_2_lots

)
from openprocurement.auctions.core.utils import get_related_award_of_contract

from openprocurement.auctions.swiftsure.tests import fixtures
from openprocurement.auctions.swiftsure.tests.base import (
    BaseAuctionWebTest, test_bids, test_lots
)

DOCUMENTS = {
    'contract': {
        'name': 'contract_signed.pdf',
        'type': 'contractSigned',
        'description': 'contract signed'
    },
    'rejection': {
        'name': 'rejection_protocol.pdf',
        'type': 'rejectionProtocol',
        'description': 'rejection protocol'
    },
    'act': {
        'name': 'act.pdf',
        'type': 'act',
        'description': 'act'
    }
}


class AuctionContractResourceTest(
    BaseAuctionWebTest,
    AuctionContractResourceTestMixin,
    AuctionContractV3_1ResourceTestCaseMixin
):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractResourceTest, self).setUp()
        # Create award
        self.award_contract_id = None
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id

    def upload_contract_document(self, contract, doc_type):
        # Uploading contract document
        response = self.app.post('/auctions/{}/contracts/{}/documents'.format(
            self.auction_id, contract['id']), upload_files=[
            ('file', DOCUMENTS[doc_type]['name'], 'content')
        ])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual(
            DOCUMENTS[doc_type]['name'], response.json["data"]["title"]
        )

        # Patching it's documentType to needed one
        response = self.app.patch_json(
            '/auctions/{}/contracts/{}/documents/{}'.format(
                self.auction_id, contract['id'], doc_id
            ),
            {"data": {
                "description": DOCUMENTS[doc_type]['description'],
                "documentType": DOCUMENTS[doc_type]['type']
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(
            response.json["data"]["documentType"], DOCUMENTS[doc_type]['type']
        )

    def check_related_award_status(self, contract, status):
        # Checking related award status
        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        contract = self.app.get('/auctions/{}/contracts/{}'.format(
            self.auction_id, contract['id']
        )).json['data']

        award = get_related_award_of_contract(
            contract, {'awards': response.json['data']}
        )

        response = self.app.get('/auctions/{}/awards/{}'.format(
            self.auction_id, award['id']
        ))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["status"], status)


@unittest.skip("option not available")
class Auction2LotContractResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots
    test_patch_auction_contract = snitch(patch_auction_contract_2_lots)

    def setUp(self):
        super(Auction2LotContractResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id
        ), {'data': {
            'suppliers': [self.initial_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']
        self.app.patch_json('/auctions/{}/awards/{}'.format(
            self.auction_id, self.award_id), {"data": {"status": "active"}}
        )


class AuctionContractDocumentResourceTest(
    BaseAuctionWebTest,
    AuctionContractDocumentResourceTestMixin
):
    initial_status = 'active.auction'
    initial_bids = test_bids
    docservice = True

    def setUp(self):
        super(AuctionContractDocumentResourceTest, self).setUp()
        # Create award
        self.award_contract_id = None
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
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id
        ), {'data': {
            'suppliers': [self.initial_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']
        self.app.patch_json('/auctions/{}/awards/{}'.format(
            self.auction_id, self.award_id), {"data": {"status": "active"}}
        )
        # Create contract for award
        response = self.app.post_json('/auctions/{}/contracts'.format(
            self.auction_id
        ), {'data': {
            'title': 'contract title',
            'description': 'contract description',
            'awardID': self.award_id
        }})
        contract = response.json['data']
        self.contract_id = contract['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionContractResourceTest))
    tests.addTest(unittest.makeSuite(AuctionContractDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
