# -*- coding: utf-8 -*-
import json
import os
from datetime import timedelta, datetime
from uuid import uuid4

from webtest import TestApp

from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.core.tests.base import PrefixedRequestClass

import openprocurement.auctions.swiftsure.tests.base as base_test
from openprocurement.auctions.swiftsure.tests.base import test_auction_data as base_test_auction_data, test_bids
from openprocurement.auctions.swiftsure.tests.tender import BaseAuctionWebTest

now = datetime.now()

test_auction_data = base_test_auction_data.copy()

bid = {
    "data": {
        "tenderers": [
            {
                "address": {
                    "countryName": "Україна",
                    "locality": "м. Вінниця",
                    "postalCode": "21100",
                    "region": "м. Вінниця",
                    "streetAddress": "вул. Островського, 33"
                },
                "contactPoint": {
                    "email": "soleksuk@gmail.com",
                    "name": "Сергій Олексюк",
                    "telephone": "+380 (432) 21-69-30"
                },
                "identifier": {
                    "scheme": u"UA-EDR",
                    "id": u"00137256",
                    "uri": u"http://www.sc.gov.ua/"
                },
                "name": "ДКП «Школяр»"
            }
        ],
        "status": "draft",
        "qualified": True,
        "value": {
            "amount": 500
        }
    }
}

bid2 = {
    "data": {
        "tenderers": [
            {
                "address": {
                    "countryName": "Україна",
                    "locality": "м. Львів",
                    "postalCode": "79013",
                    "region": "м. Львів",
                    "streetAddress": "вул. Островського, 34"
                },
                "contactPoint": {
                    "email": "aagt@gmail.com",
                    "name": "Андрій Олексюк",
                    "telephone": "+380 (322) 91-69-30"
                },
                "identifier": {
                    "scheme": u"UA-EDR",
                    "id": u"00137226",
                    "uri": u"http://www.sc.gov.ua/"
                },
                "name": "ДКП «Книга»"
            }
        ],
        "qualified": True,
        "value": {
            "amount": 501
        }
    }
}

question = {
    "data": {
        "author": {
            "address": {
                "countryName": "Україна",
                "locality": "м. Вінниця",
                "postalCode": "21100",
                "region": "м. Вінниця",
                "streetAddress": "вул. Островського, 33"
            },
            "contactPoint": {
                "email": "soleksuk@gmail.com",
                "name": "Сергій Олексюк",
                "telephone": "+380 (432) 21-69-30"
            },
            "identifier": {
                "id": "00137226",
                "legalName": "Державне комунальне підприємство громадського харчування «Школяр»",
                "scheme": "UA-EDR",
                "uri": "http://sch10.edu.vn.ua/"
            },
            "name": "ДКП «Школяр»"
        },
        "description": "Просимо додати таблицю потрібної калорійності харчування",
        "title": "Калорійність"
    }
}

answer = {
    "data": {
        "answer": "Таблицю додано в файлі \"Kalorijnist.xslx\""
    }
}

cancellation = {
    'data': {
        'reason': 'cancellation reason'
    }
}

prolongation_short = {
    'decisionID': 'ZM-937-99-92',
    'description': 'Prolongation description',
    'reason': 'other',
    'documents': [],
    'datePublished': get_now().isoformat(),
}

prolongation_long = {
    'decisionID': 'ZM-937-99-92-2',
    'description': 'Long prolongation description',
    'reason': 'other',
    'documents': [],
    'datePublished': get_now().isoformat(),
}

test_max_uid = uuid4().hex

test_auction_maximum_data = test_auction_data.copy()
test_auction_maximum_data.update({
    "title_en": u"Cases with state awards",
    "title_ru": u"футляры к государственным наградам",
    "procuringEntity": {
        "name": u"Державне управління справами",
        "identifier": {
            "scheme": u"UA-EDR",
            "id": u"00037256",
            "uri": u"http://www.dus.gov.ua/"
        },
        "address": {
            "countryName": u"Україна",
            "postalCode": u"01220",
            "region": u"м. Київ",
            "locality": u"м. Київ",
            "streetAddress": u"вул. Банкова, 11, корпус 1"
        },
        "contactPoint": {
            "name": u"Державне управління справами",
            "telephone": u"0440000000"
        },
        'kind': 'general'
    },
    "items": [
        {
            "id": test_max_uid,
            "description": u"Земля для військовослужбовців",
            "classification": {
                "scheme": u"CAV",
                "id": u"06000000-2",
                "description": u"Земельні ділянки"
            },
            "unit": {
                "name": u"item",
                "code": u"44617100-9"
            },
            "quantity": 5
        }
    ],
})


test_complaint_data = {'data':
        {
            'title': 'complaint title',
            'description': 'complaint description',
            'author': bid["data"]["tenderers"][0]
        }
    }


class DumpsTestAppwebtest(TestApp):
    def do_request(self, req, status=None, expect_errors=None):
        req.headers.environ["HTTP_HOST"] = "api-sandbox.ea.openprocurement.org"
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            self.file_obj.write(req.as_bytes(True))
            self.file_obj.write("\n")
            if req.body:
                try:
                    self.file_obj.write(
                        '\n' + json.dumps(json.loads(req.body), indent=2, ensure_ascii=False).encode('utf8'))
                    self.file_obj.write("\n")
                except:
                    pass
            self.file_obj.write("\n")
        resp = super(DumpsTestAppwebtest, self).do_request(req, status=status, expect_errors=expect_errors)
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            headers = [(n.title(), v)
                       for n, v in resp.headerlist
                       if n.lower() != 'content-length']
            headers.sort()
            self.file_obj.write(str('\n%s\n%s\n') % (
                resp.status,
                str('\n').join([str('%s: %s') % (n, v) for n, v in headers]),
            ))

            if resp.testbody:
                try:
                    self.file_obj.write('\n' + json.dumps(json.loads(resp.testbody), indent=2, ensure_ascii=False).encode('utf8'))
                except:
                    pass
            self.file_obj.write("\n\n")
        return resp


class AuctionResourceTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    initial_bids = test_bids
    docservice = True

    def setUp(self):
        self.app = DumpsTestAppwebtest(
            "config:tests.ini", relative_to=os.path.dirname(base_test.__file__))
        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('broker', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        if self.docservice:
            self.setUpDS()
            self.app.app.registry.docservice_url = 'http://public.docs-sandbox.ea.openprocurement.org'

    def generate_docservice_url(self):
        return super(AuctionResourceTest, self).generate_docservice_url().replace('/localhost/', '/public.docs-sandbox.ea.openprocurement.org/')

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

    def test_docs_acceleration(self):
        # SANDBOX_MODE=TRUE
        data = test_auction_data.copy()
        data['procurementMethodDetails'] = 'quick, accelerator=1440'
        data['submissionMethodDetails'] = 'test submissionMethodDetails'
        data['mode'] = 'test'
        data["auctionPeriod"] = {
            "startDate": (now + timedelta(minutes=5)).isoformat()
        }
        self.app.authorization = ('Basic', ('broker3', ''))

        with open('docs/source/tutorial/auction-post-acceleration.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')
        auction = response.json['data']
        self.auction_id = auction['id']
        owner_token = response.json['access']['token']

    def test_docs_2pc(self):
        # Creating auction in draft status
        #
        data = test_auction_data.copy()
        data['status'] = 'draft'
        self.app.authorization = ('Basic', ('broker3', ''))

        with open('docs/source/tutorial/auction-post-2pc.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')

        auction = response.json['data']
        self.auction_id = auction['id']
        owner_token = response.json['access']['token']

        # switch to 'active.tendering'

        with open('docs/source/tutorial/auction-patch-2pc.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token),
                                           {'data': {"status": 'active.tendering'}})
            self.assertEqual(response.status, '200 OK')

    def test_docs_one_bidder_tutorial(self):
        request_path = '/auctions?opt_pretty=1'

        # Creating auction
        #
        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.post_json(
            '/auctions?opt_pretty=1', {"data": test_auction_data})
        self.assertEqual(response.status, '201 Created')
        auction = response.json['data']
        auction_id = self.auction_id = response.json['data']['id']
        used_transfer_token = response.json['access']['transfer']

        with open('docs/source/tutorial/retrieve-auction-json-data.http', 'w') as self.app.file_obj:
            self.app.authorization = ('Basic', ('broker', ''))
            response = self.app.get('/auctions/{}'.format(auction_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker3', ''))

        with open('docs/source/tutorial/create_transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')

        transfer = response.json

        with open('docs/source/tutorial/retrieve_transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['data']['id']))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')

        req_data = {"data": {"id": transfer['data']['id'],
                             'transfer': used_transfer_token}}

        with open('docs/source/tutorial/transfer_token.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions/{}/ownership'.format(auction_id), req_data
            )
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(
                response.json['data']['owner'], self.app.authorization[1][0]
            )

        with open('docs/source/tutorial/retrieve_used_transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['data']['id']))
            self.assertIn('usedFor', response.json['data'])
            self.assertEqual(
                '/auctions/{}'.format(auction_id), response.json['data']['usedFor']
            )
            owner_token = transfer['access']['token']

        with open('docs/source/tutorial/blank-auction-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction['id']))
            self.assertEqual(response.status, '200 OK')

        self.app.get('/auctions')
        with open('docs/source/tutorial/initial-auction-listing.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions')
            self.assertEqual(response.status, '200 OK')

        # Enquiries
        #
        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/tutorial/ask-question.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/questions'.format(
                auction_id), question, status=201)
            question_id = response.json['data']['id']
            self.assertEqual(response.status, '201 Created')

        self.app.authorization = ('Basic', ('broker3', ''))
        with open('docs/source/tutorial/answer-question.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/questions/{}?acc_token={}'.format(
                auction_id, question_id, owner_token), answer, status=200)
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/list-question.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/questions'.format(
                auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/get-answer.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/questions/{}'.format(
                auction_id, question_id))
            self.assertEqual(response.status, '200 OK')

        # One bid submit

        self.app.authorization = ('Basic', ('broker', ''))
        bids_access = {}

        with open('docs/source/tutorial/register-bidder.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                          {'data': {'tenderers': [self.initial_organization], "status": "draft", "value": {"amount": 500}, 'qualified': True}})

            self.assertEqual(response.status, '201 Created')
            bid1_id = response.json['data']['id']
            bids_access[bid1_id] = response.json['access']['token']

        with open('docs/source/tutorial/activate-bidder.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
                self.auction_id, bid1_id, bids_access[bid1_id]), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['status'], "active")



        with open('docs/source/tutorial/upload-bid-proposal.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(self.auction_id, bid1_id, bids_access[bid1_id]),
                {'data': {
                    'title': u'Proposal.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/bidder-documents.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/bids/{}/documents?acc_token={}'.format(
                self.auction_id, bid1_id, bids_access[bid1_id]))
            self.assertEqual(response.status, '200 OK')

        # switch to active.qualification
        self.set_status('active.auction', {"auctionPeriod": {"startDate": None}, 'status': 'active.tendering'})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"id": auction_id}})
        # get awards
        self.app.authorization = ('Basic', ('broker3', ''))
        with open('docs/source/tutorial/get-award.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
            self.assertEqual(response.status, '200 OK')

        # get pending award
        award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending.admission'][0]
        award_date = [i['date'] for i in response.json['data'] if i['status'] == 'pending.admission'][0]

        # uploading admission protocol
        with open('docs/source/tutorial/upload-admission-protocol.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
                self.auction_id, award_id, owner_token),
                {'data': {
                    'title': u'admission_protocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "auctionProtocol",
                }})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')

        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('admission_protocol.pdf', response.json["data"]["title"])
        # update protocol
        with open('docs/source/tutorial/patch-admission-protocol.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, owner_token), {"data": {
                "description": "admission protocol",
                "documentType": 'admissionProtocol'
            }})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["data"]["documentType"], 'admissionProtocol')
            self.assertEqual(response.json["data"]["author"], 'auction_owner')

        with open('docs/source/tutorial/update-award-to-pending.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
                                           {"data": {"status": "pending"}})
            self.assertNotEqual(response.json['data']['date'], award_date)

        with open('docs/source/tutorial/bidder-auction-protocol.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, owner_token),
                {'data': {
                    'title': u'SignedAuctionProtocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "auctionProtocol",
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/update-bidder-auction-protocol.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, owner_token), {"data": {
                "description": "auction protocol",
                "documentType": 'auctionProtocol'
            }})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
            self.assertEqual(response.json["data"]["author"], 'auction_owner')

        with open('docs/source/tutorial/confirm-qualification.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(self.auction_id, award_id, owner_token), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')

        # get contract id
        with open('docs/source/tutorial/get-contract.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction_id))
            contract_id = response.json['data']['contracts'][-1]['id']

        # signing contract
        # uploading contract
        with open('docs/source/tutorial/auction-contract-upload-document.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(
                self.auction_id, contract_id, owner_token), {'data': {
                    'title': u'contract_signed.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')

        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('contract_signed.pdf', response.json["data"]["title"])

        with open('docs/source/tutorial/signing-contract.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(self.auction_id, contract_id, doc_id, owner_token),
                {"data": {
                    "description": "contract signed",
                    "documentType": 'contractSigned'
                }})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["data"]["documentType"], 'contractSigned')

        # setting dateSigned field
        signature_date = get_now().isoformat()
        with open('docs/source/tutorial/auction-contract-sign.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
                self.auction_id, contract_id, owner_token
            ), {"data": {"dateSigned": signature_date}})
            self.assertEqual(response.status, '200 OK')

        # set contract as active
        with open('docs/source/tutorial/activate-contract.http', 'w') as self.app.file_obj:
            self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token), {"data": {"status": "active"}})

        # check status
        with open('docs/source/tutorial/check-contract-status.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction_id))
            self.assertEqual(response.json['data']['status'], 'complete')


    def test_docs_two_bidders_tutorial(self):
        request_path = '/auctions?opt_pretty=1'

        # Creating auction
        #
        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.post_json(
            '/auctions?opt_pretty=1', {"data": test_auction_data})
        self.assertEqual(response.status, '201 Created')
        auction = response.json['data']
        auction_id = self.auction_id = response.json['data']['id']
        used_transfer_token = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.get('/auctions/{}'.format(auction_id))
        self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker3', ''))

        response = self.app.post_json('/transfers', {"data": {}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')

        transfer = response.json

        response = self.app.get('/transfers/{}'.format(transfer['data']['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')

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

        with open('docs/source/tutorial/blank-auction-2bidders-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction['id']))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))
        bids_access = {}

        with open('docs/source/tutorial/2bidders-register-first-bidder.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                          {'data': {'tenderers': [self.initial_organization], "status": "draft", "value": {"amount": 500}, 'qualified': True}})

            self.assertEqual(response.status, '201 Created')
            bid1_id = response.json['data']['id']
            bids_access[bid1_id] = response.json['access']['token']

        with open('docs/source/tutorial/2bidders-activate-bidder.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
                auction_id, bid1_id, bids_access[bid1_id]), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['status'], "active")

        with open('docs/source/tutorial/2bidders-upload-bid-proposal.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(auction_id, bid1_id, bids_access[bid1_id]),
                {'data': {
                    'title': u'Proposal.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        response = self.app.get('/auctions/{}/bids/{}/documents?acc_token={}'.format(
            auction_id, bid1_id, bids_access[bid1_id]))
        self.assertEqual(response.status, '200 OK')

        # Second bidder registration
        #

        with open('docs/source/tutorial/register-2nd-bidder.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids'.format(auction_id), 
                                        {'data': {'tenderers': [self.initial_organization], "status": "draft", "value": {"amount": 300}, 'qualified': True}})

            bid2_id = response.json['data']['id']
            bids_access[bid2_id] = response.json['access']['token']
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/2bidders-activate-second-bidder.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
                auction_id, bid2_id, bids_access[bid2_id]), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['status'], "active")

        with open('docs/source/tutorial/2bidders-upload-second-bid-proposal.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(auction_id, bid2_id, bids_access[bid2_id]),
                {'data': {
                    'title': u'Proposal.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        self.set_status('active.auction')

        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}/auction'.format(auction_id))
        auction_bids_data = response.json['data']['bids']
        patch_data = {
            'auctionUrl': u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(auction_id),
            'bids': [
                {
                    "id": bid1_id,
                    "participationUrl": 'https://auction.auction.url/for_bid/{}'.format(bid1_id)
                    },
                {
                    "id": bid2_id,
                    "participationUrl": 'https://auction.auction.url/for_bid/{}'.format(bid2_id)
                }
            ]
        }
        response = self.app.patch_json('/auctions/{}/auction?acc_token={}'.format(auction_id, owner_token),
                                       {'data': patch_data})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/auction-url.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction_id))
            self.assertEqual(response.status, '200 OK')

        # view bid participationUrl

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/tutorial/bidder-participation-url.http', 'w') as self.app.file_obj:
            response = self.app.get(
                '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid1_id, bids_access[bid1_id]))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['participationUrl'], 'https://auction.auction.url/for_bid/{}'.format(bid1_id))

        with open('docs/source/tutorial/bidder2-participation-url.http', 'w') as self.app.file_obj:
            response = self.app.get(
                '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid2_id, bids_access[bid2_id]))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['participationUrl'], 'https://auction.auction.url/for_bid/{}'.format(bid2_id))


        # posting auction results
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                      {'data': {'bids': auction_bids_data}})
        # get awards
        self.app.authorization = ('Basic', ('broker3', ''))

        with open('docs/source/qualification/awards-get.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
            self.assertEqual(response.status, '200 OK')

        award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
        award_id2 = [i['id'] for i in response.json['data'] if i['status'] == 'pending.waiting'][0]

        # cancel pending.waiting award
        self.app.authorization = ('Basic', ('broker', ''))
        with open('docs/source/qualification/award-waiting-cancel.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id2, bids_access[bid2_id]), {"data": {"status": "cancelled"}})
            self.assertEqual(response.status, '200 OK')

        # first award qualification
        self.app.authorization = ('Basic', ('broker3', ''))
        with open('docs/source/qualification/award-pending-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
                self.auction_id, award_id, owner_token), {'data': {
                    'title': u'auction_protocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            doc_id = response.json["data"]['id']

        with open('docs/source/qualification/patch-award.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, owner_token),
                {"data": {
                    "description": "auction protocol",
                    "documentType": 'auctionProtocol'
                }})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
            self.assertEqual(response.json["data"]["author"], 'auction_owner')



        with open('docs/source/qualification/confirm-qualification-2bids.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(self.auction_id, award_id, owner_token), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')


        # get contract id
        with open('docs/source/tutorial/get-contract-2bids.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction_id))
            contract_id = response.json['data']['contracts'][-1]['id']


        # uploading contract
        with open('docs/source/tutorial/auction-contract-upload-document-2bids.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(
                self.auction_id, contract_id, owner_token), {'data': {
                    'title': u'contract_signed.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')

        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('contract_signed.pdf', response.json["data"]["title"])

        with open('docs/source/tutorial/auction-contract-get-documents-2bids.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/contracts/{}/documents'.format(
                self.auction_id, contract_id))
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/auction-contract-upload-second-document-2bids.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, contract_id, owner_token),
                {'data': {
                    'title': u'contract_second_document.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                }})
            self.assertEqual(response.status, '201 Created')


        with open('docs/source/tutorial/auction-contract-get-documents-again-2bids.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/contracts/{}/documents'.format(
                self.auction_id, contract_id))
        self.assertEqual(response.status, '200 OK')

        # signing contract
        with open('docs/source/tutorial/signing-contract-2bids.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(self.auction_id, contract_id, doc_id, owner_token),
                {"data": {
                    "description": "contract signed",
                    "documentType": 'contractSigned'
                }})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["data"]["documentType"], 'contractSigned')

        # setting dateSigned field
        signature_date = get_now().isoformat()
        with open('docs/source/tutorial/auction-contract-sign-2bids.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
                self.auction_id, contract_id, owner_token
            ), {"data": {"dateSigned": signature_date}})
            self.assertEqual(response.status, '200 OK')

        # set contract as active
        with open('docs/source/tutorial/activate-contract-2bids.http', 'w') as self.app.file_obj:
            self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token), {"data": {"status": "active"}})

        # check status
        with open('docs/source/tutorial/check-contract-status-2bids.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction_id))
            self.assertEqual(response.json['data']['status'], 'complete')

    def test_award_unsuccessfull(self):
        request_path = '/auctions?opt_pretty=1'

        # Creating auction
        #
        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.post_json(
            '/auctions?opt_pretty=1', {"data": test_auction_data})
        self.assertEqual(response.status, '201 Created')
        auction = response.json['data']
        auction_id = self.auction_id = response.json['data']['id']
        used_transfer_token = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.get('/auctions/{}'.format(auction_id))
        self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker3', ''))
        owner_token = self.change_ownership(auction_id, used_transfer_token)

        self.app.authorization = ('Basic', ('broker', ''))
        bids_access = {}

        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "status": "draft", "value": {"amount": 500}, 'qualified': True}})

        self.assertEqual(response.status, '201 Created')
        bid1_id = response.json['data']['id']
        bids_access[bid1_id] = response.json['access']['token']

        response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
            auction_id, bid1_id, bids_access[bid1_id]), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], "active")

        response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(auction_id, bid1_id, bids_access[bid1_id]),
            {'data': {
                'title': u'Proposal.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
            }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.get('/auctions/{}/bids/{}/documents?acc_token={}'.format(
            auction_id, bid1_id, bids_access[bid1_id]))
        self.assertEqual(response.status, '200 OK')

        # Second bidder registration
        #

        response = self.app.post_json('/auctions/{}/bids'.format(auction_id), 
                                    {'data': {'tenderers': [self.initial_organization], "status": "draft", "value": {"amount": 300}, 'qualified': True}})

        bid2_id = response.json['data']['id']
        bids_access[bid2_id] = response.json['access']['token']
        self.assertEqual(response.status, '201 Created')

        response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
            auction_id, bid2_id, bids_access[bid2_id]), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], "active")

        response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(auction_id, bid2_id, bids_access[bid2_id]),
            {'data': {
                'title': u'Proposal.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
            }})
        self.assertEqual(response.status, '201 Created')

        self.set_status('active.auction')

        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}/auction'.format(auction_id))
        auction_bids_data = response.json['data']['bids']
        patch_data = {
            'auctionUrl': u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(auction_id),
            'bids': [
                {
                    "id": bid1_id,
                    "participationUrl": 'https://auction.auction.url/for_bid/{}'.format(bid1_id)
                    },
                {
                    "id": bid2_id,
                    "participationUrl": 'https://auction.auction.url/for_bid/{}'.format(bid2_id)
                }
            ]
        }
        response = self.app.patch_json('/auctions/{}/auction?acc_token={}'.format(auction_id, owner_token),
                                       {'data': patch_data})
        self.assertEqual(response.status, '200 OK')

        response = self.app.get('/auctions/{}'.format(auction_id))
        self.assertEqual(response.status, '200 OK')

        # view bid participationUrl
        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.get(
            '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid1_id, bids_access[bid1_id]))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['participationUrl'], 'https://auction.auction.url/for_bid/{}'.format(bid1_id))

        response = self.app.get(
            '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid2_id, bids_access[bid2_id]))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['participationUrl'], 'https://auction.auction.url/for_bid/{}'.format(bid2_id))

        # posting auction results
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                      {'data': {'bids': auction_bids_data}})
        # get awards
        self.app.authorization = ('Basic', ('broker3', ''))

        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')

        award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
        award_id2 = [i['id'] for i in response.json['data'] if i['status'] == 'pending.waiting'][0]

        # set award as unsuccessful
        # upload rejection protocol
        with open('docs/source/qualification/award-active-unsuccessful-upload.http', 'w') as self.app.file_obj:
            response = self.app.post(
                '/auctions/{}/awards/{}/documents?acc_token={}'.format(
                    self.auction_id, award_id, owner_token
                ), upload_files=[('file', 'rejection_protocol.pdf', 'content')])
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            doc_id = response.json["data"]['id']
            self.assertIn(doc_id, response.headers['Location'])
            self.assertEqual(
                'rejection_protocol.pdf', response.json["data"]["title"]
            )
        with open('docs/source/qualification/patch-award-active-unsuccessful.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(
                    self.auction_id, award_id, doc_id, owner_token
                ),
                {"data": {
                    "description": "rejection protocol",
                    "documentType": 'rejectionProtocol'
                }})

            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(doc_id, response.json["data"]["id"])
            self.assertIn("documentType", response.json["data"])
            self.assertEqual(
                response.json["data"]["documentType"], 'rejectionProtocol'
            )

        with open('docs/source/qualification/award-pending-unsuccessful.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id, owner_token), {"data":{"status":"unsuccessful"}})
            self.assertEqual(response.status, '200 OK')


        # Preparing the cancellation request
        #

        self.set_status('active.awarded')
        with open('docs/source/tutorial/prepare-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
                self.auction_id, owner_token), cancellation)
            self.assertEqual(response.status, '201 Created')

        cancellation_id = response.json['data']['id']

        # Filling cancellation with protocol and supplementary documentation
        #

        with open('docs/source/tutorial/upload-cancellation-doc.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/cancellations/{}/documents?acc_token={}'.format(self.auction_id, cancellation_id, owner_token),
                {'data': {
                    'title': u'Notice.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            cancellation_doc_id = response.json['data']['id']
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/patch-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(
                self.auction_id, cancellation_id, cancellation_doc_id, owner_token), {'data': {"description": 'Changed description'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/update-cancellation-doc.http', 'w') as self.app.file_obj:
            response = self.app.put_json('/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(self.auction_id, cancellation_id, cancellation_doc_id, owner_token),
                {'data': {
                    'title': u'Cancelation doc.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '200 OK')

        # Activating the request and cancelling auction
        #

        with open('docs/source/tutorial/active-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/cancellations/{}?acc_token={}'.format(
                self.auction_id, cancellation_id, owner_token), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')


    def _test_docs_complaints(self):

        ###################### Tender Conditions Claims/Complaints ##################
        #
        #### Claim Submission (with documents)
        #

        self.create_auction()

        with open('docs/source/complaints/complaint-submission.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/complaints'.format(
                self.auction_id), test_complaint_data)
            self.assertEqual(response.status, '201 Created')

        complaint1_id = response.json['data']['id']
        complaint1_token = response.json['access']['token']

        with open('docs/source/complaints/complaint-submission-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/complaints/{}/documents?acc_token={}'.format(
                    self.auction_id, complaint1_id, complaint1_token), {'data': {
                    'title': u'Complaint_Attachement.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/complaints/complaint-claim.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, complaint1_id, complaint1_token), {"data":{"status":"claim"}})
            self.assertEqual(response.status, '200 OK')

        #### Claim Submission (without documents)
        #

        test_complaint_data['data']['status'] = 'claim'

        with open('docs/source/complaints/complaint-submission-claim.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/complaints'.format(
                self.auction_id), test_complaint_data)
            self.assertEqual(response.status, '201 Created')

        complaint2_id = response.json['data']['id']
        complaint2_token = response.json['access']['token']

        #### Tender Conditions Claim/Complaint Retrieval
        #

        with open('docs/source/complaints/complaints-list.http', 'w') as self.app.file_obj:
            self.app.authorization = None
            response = self.app.get('/auctions/{}/complaints'.format(self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/complaint.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/complaints/{}'.format(self.auction_id, complaint1_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        #### Claim's Answer
        #

        with open('docs/source/complaints/complaint-answer.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(self.auction_id, complaint1_id, self.auction_token),
                {
                    "data": {
                        "status": "answered",
                        "resolutionType": "resolved",
                        "tendererAction": "Виправлено неконкурентні умови",
                        "resolution": "Виправлено неконкурентні умови"
                    }
                }
            )
            self.assertEqual(response.status, '200 OK')


        #### Satisfied Claim
        #

        with open('docs/source/complaints/complaint-satisfy.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, complaint1_id, complaint1_token), {"data":{"status":"resolved","satisfied":True}})
            self.assertEqual(response.status, '200 OK')

        #### Satisfied Claim
        #


        response = self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, complaint2_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/complaint-escalate.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, complaint2_id, complaint2_token), {"data":{"status":"pending","satisfied":False}})
            self.assertEqual(response.status, '200 OK')

        #### Rejecting Tender Conditions Complaint
        #

        self.app.authorization = ('Basic', ('reviewer', ''))

        with open('docs/source/complaints/complaint-reject.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}'.format(
                    self.auction_id, complaint2_id), {"data":{"status":"invalid"}})
            self.assertEqual(response.status, '200 OK')

        #### Submitting Tender Conditions Complaint Resolution
        #

        self.app.authorization = ('Basic', ('broker', ''))


        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), test_complaint_data)
        self.assertEqual(response.status, '201 Created')
        complaint3_id = response.json['data']['id']
        complaint3_token = response.json['access']['token']
        self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, complaint3_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, complaint3_id, complaint3_token), {"data":{"status":"pending","satisfied":False}})

        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), test_complaint_data)
        self.assertEqual(response.status, '201 Created')
        del test_complaint_data['data']['status']
        complaint4_id = response.json['data']['id']
        complaint4_token = response.json['access']['token']
        self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, complaint4_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.app.patch_json('/auctions/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, complaint4_id, complaint4_token), {"data":{"status":"pending","satisfied":False}})


        self.app.authorization = ('Basic', ('reviewer', ''))

        with open('docs/source/complaints/complaint-resolution-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/complaints/{}/documents'.format(
                    self.auction_id, complaint3_id), {'data': {
                    'title': u'ComplaintResolution.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/complaints/complaint-resolve.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}'.format(
                    self.auction_id, complaint3_id), {"data":{"status":"resolved"}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/complaint-decline.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/complaints/{}'.format(
                    self.auction_id, complaint4_id), {"data":{"status":"declined"}})
            self.assertEqual(response.status, '200 OK')

        # create bids
        self.set_status('active.tendering')
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.post_json('/auctions/{}/bids'.format(self.auction_id),
                                      {'data': {"qualified": True, 'tenderers': [bid["data"]["tenderers"][0]], "value": {"amount": 450}}})
        bid_id = response.json['data']['id']
        bid_token = response.json['access']['token']
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.post_json('/auctions/{}/bids'.format(self.auction_id),
                                      {'data': {"qualified": True, 'tenderers': [bid["data"]["tenderers"][0]], "value": {"amount": 475}}})
        # get auction info
        self.set_status('active.auction')
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}/auction'.format(self.auction_id))
        auction_bids_data = response.json['data']['bids']
        # posting auction urls
        response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id),
                                       {
                                           'data': {
                                               'auctionUrl': 'https://auction.auction.url',
                                               'bids': [
                                                   {
                                                       'id': i['id'],
                                                       'participationUrl': 'https://auction.auction.url/for_bid/{}'.format(i['id'])
                                                   }
                                                   for i in auction_bids_data
                                               ]
                                           }
        })
        # posting auction results
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                      {'data': {'bids': auction_bids_data}})
        # get awards
        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/qualification/awards-get.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
            self.assertEqual(response.status, '200 OK')

        award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

        with open('docs/source/qualification/award-pending-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
                self.auction_id, award_id, self.auction_token), {'data': {
                    'title': u'Unsuccessful_Reason.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/qualification/award-pending-unsuccessful.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id, self.auction_token), {"data":{"status":"unsuccessful"}})
            self.assertEqual(response.status, '200 OK')

        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        award_id2 = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

        with open('docs/source/qualification/award-pending-active.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id2, self.auction_token), {"data":{"status":"active"}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/qualification/award-active-get.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards/{}'.format(
                self.auction_id, award_id2))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/qualification/award-active-cancel.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id2, self.auction_token), {"data":{"status":"cancelled"}})
            self.assertEqual(response.status, '200 OK')

        response = self.app.get('/auctions/{}/awards?acc_token={}'.format(self.auction_id, self.auction_token))
        award_id3 = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

        with open('docs/source/qualification/award-active-cancel-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
                self.auction_id, award_id3, self.auction_token), {'data': {
                    'title': u'Disqualified_reason.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "notice",
                    "description": "Disqualified reason"
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/qualification/award-active-cancel-disqualify.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id3, self.auction_token), {"data":{"status":"unsuccessful", "title": "Disqualified", "description": "Candidate didn’t sign the auction protocol in 3 business days"}})
            self.assertEqual(response.status, '200 OK')

        ###################### Tender Award Claims/Complaints ##################
        #

        #### Tender Award Claim Submission (with documents)
        #

        with open('docs/source/complaints/award-complaint-submission.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(
                self.auction_id, award_id, bid_token), test_complaint_data)
            self.assertEqual(response.status, '201 Created')

        complaint1_id = response.json['data']['id']
        complaint1_token = response.json['access']['token']

        with open('docs/source/complaints/award-complaint-submission-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/complaints/{}/documents?acc_token={}'.format(
                    self.auction_id, award_id, complaint1_id, complaint1_token), {'data': {
                    'title': u'Complaint_Attachement.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/complaints/award-complaint-claim.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, award_id, complaint1_id, complaint1_token), {"data":{"status":"claim"}})
            self.assertEqual(response.status, '200 OK')

        #### Tender Award Claim Submission (without documents)
        #

        test_complaint_data['data']['status'] = 'claim'

        with open('docs/source/complaints/award-complaint-submission-claim.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(
                self.auction_id, award_id, bid_token), test_complaint_data)
            self.assertEqual(response.status, '201 Created')

        complaint2_id = response.json['data']['id']
        complaint2_token = response.json['access']['token']

        #### Tender Award Claim/Complaint Retrieval
        #

        with open('docs/source/complaints/award-complaints-list.http', 'w') as self.app.file_obj:
            self.app.authorization = None
            response = self.app.get('/auctions/{}/awards/{}/complaints'.format(self.auction_id, award_id,))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/award-complaint.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards/{}/complaints/{}'.format(self.auction_id, award_id, complaint1_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        #### Claim's Answer
        #

        with open('docs/source/complaints/award-complaint-answer.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(self.auction_id, award_id, complaint1_id, self.auction_token),
                {
                    "data": {
                        "status": "answered",
                        "resolutionType": "resolved",
                        "tendererAction": "Виправлено неконкурентні умови",
                        "resolution": "Виправлено неконкурентні умови"
                    }
                }
            )
            self.assertEqual(response.status, '200 OK')


        #### Satisfied Claim
        #

        with open('docs/source/complaints/award-complaint-satisfy.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, award_id, complaint1_id, complaint1_token), {"data":{"status":"resolved","satisfied":True}})
            self.assertEqual(response.status, '200 OK')

        #### Satisfied Claim
        #
        response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, award_id, complaint2_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/award-complaint-escalate.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                    self.auction_id, award_id, complaint2_id, complaint2_token), {"data":{"status":"pending","satisfied":False}})
            self.assertEqual(response.status, '200 OK')

        #### Rejecting Tender Award Complaint
        #

        self.app.authorization = ('Basic', ('reviewer', ''))

        with open('docs/source/complaints/award-complaint-reject.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}'.format(
                    self.auction_id, award_id, complaint2_id), {"data":{"status":"invalid"}})
            self.assertEqual(response.status, '200 OK')

        #### Submitting Tender Award Complaint Resolution
        #

        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(
            self.auction_id, award_id, bid_token), test_complaint_data)
        self.assertEqual(response.status, '201 Created')
        complaint3_id = response.json['data']['id']
        complaint3_token = response.json['access']['token']
        self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, award_id, complaint3_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, award_id, complaint3_id, complaint3_token), {"data":{"status":"pending","satisfied":False}})


        response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(
            self.auction_id, award_id, bid_token), test_complaint_data)
        self.assertEqual(response.status, '201 Created')
        complaint4_id = response.json['data']['id']
        complaint4_token = response.json['access']['token']
        self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, award_id, complaint4_id, self.auction_token), {"data":{"status":"answered","resolutionType":"resolved","resolution":"Виправлено неконкурентні умови"}})
        self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(
                self.auction_id, award_id, complaint4_id, complaint4_token), {"data":{"status":"pending","satisfied":False}})

        self.app.authorization = ('Basic', ('reviewer', ''))

        with open('docs/source/complaints/award-complaint-resolution-upload.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/complaints/{}/documents'.format(
                    self.auction_id, award_id, complaint3_id), {'data': {
                    'title': u'ComplaintResolution.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/complaints/award-complaint-resolve.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}'.format(
                    self.auction_id, award_id, complaint3_id), {"data":{"status":"resolved"}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/complaints/award-complaint-decline.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}'.format(
                    self.auction_id, award_id, complaint4_id), {"data":{"status":"declined"}})
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/qualification/awards-unsuccessful-get1.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards'.format(
                self.auction_id, award_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/qualification/award-unsuccessful-cancel.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id, self.auction_token), {"data":{"status":"cancelled"}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/qualification/awards-unsuccessful-get2.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards'.format(
                self.auction_id, award_id))
            self.assertEqual(response.status, '200 OK')
