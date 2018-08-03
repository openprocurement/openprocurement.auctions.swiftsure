# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta


from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.plugins.awarding.v3_1.tests.chronograph import (
    AuctionAwardSwitchResourceTestMixin,
    AuctionDontSwitchSuspendedAuctionResourceTestMixin,
)
from openprocurement.auctions.core.tests.blanks.chronograph_blanks import (
    # AuctionSwitchAuctionResourceTest
    switch_to_auction,
    # AuctionSwitchUnsuccessfulResourceTest
    switch_to_unsuccessful,
    # AuctionComplaintSwitchResourceTest
    switch_to_pending,
    switch_to_complaint,
    # AuctionAwardComplaintSwitchResourceTest
    switch_to_pending_award,
    switch_to_complaint_award,
    # AuctionDontSwitchSuspendedAuction2ResourceTest
    switch_suspended_auction_to_auction,
    contract_signing_period_switch_to_complete,
)
from openprocurement.auctions.core.tests.plugins.awarding.v3_1.tests.blanks.chronograph_blanks import (
    # AuctionAwardSwitch2ResourceTest
    switch_verification_to_unsuccessful_2,
    switch_active_to_unsuccessful_2,
    # AuctionAwardSwitchResourceTest
    switch_admission_to_unsuccessful
)
from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.swiftsure.tests.base import (
    test_lots,
    test_bids,
    test_organization,
    BaseAuctionWebTest,
)

from openprocurement.auctions.swiftsure.tests import fixtures
from openprocurement.auctions.swiftsure.tests.blanks.chronograph_blanks import (
    # AuctionSwitchQualificationResourceTest
    switch_to_qualification,
    # AuctionAuctionPeriodResourceTest
    set_auction_period,
    reset_auction_period
)


class AuctionSwitchQualificationResourceTest(BaseAuctionWebTest):
    initial_bids = test_bids[:1]

    test_switch_to_qualification = snitch(switch_to_qualification)


class AuctionSwitchAuctionResourceTest(BaseAuctionWebTest):
    initial_bids = test_bids

    test_switch_to_auction = snitch(switch_to_auction)


class AuctionSwitchUnsuccessfulResourceTest(BaseAuctionWebTest):

    test_switch_to_unsuccessful = snitch(switch_to_unsuccessful)


@unittest.skip("option not available")
class AuctionLotSwitchQualificationResourceTest(
        AuctionSwitchQualificationResourceTest):
    initial_lots = test_lots


@unittest.skip("option not available")
class AuctionLotSwitchAuctionResourceTest(AuctionSwitchAuctionResourceTest):
    initial_lots = test_lots


@unittest.skip("option not available")
class AuctionLotSwitchUnsuccessfulResourceTest(
        AuctionSwitchUnsuccessfulResourceTest):
    initial_lots = test_lots


class AuctionAuctionPeriodResourceTest(BaseAuctionWebTest):
    initial_bids = test_bids

    test_set_auction_period = snitch(set_auction_period)
    test_reset_auction_period = snitch(reset_auction_period)


class AuctionAward2BidsSwitchResourceTest(
        BaseAuctionWebTest,
        AuctionAwardSwitchResourceTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionAward2BidsSwitchResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": b['value']
                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json(
            '/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


class AuctionAward1BidSwitchResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = [test_bids[0]]

    def setUp(self):
        super(AuctionAward1BidSwitchResourceTest, self).setUp()
        authorization = self.app.authorization
        self.set_status('active.auction', {'status': 'active.tendering'})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json(
            '/auctions/{}'.format(self.auction_id),
            {'data': {'id': self.auction_id}}
        )
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['data']['status'],
            'active.qualification')
        auction = response.json['data']
        self.award_id = auction['awards'][0]['id']
        self.app.authorization = authorization

    test_switch_admission_to_unsuccessful = snitch(
        switch_admission_to_unsuccessful)


@unittest.skip("option not available")
class AuctionAwardSwitch2ResourceTest(BaseAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 101 * (i + 1),
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True
        }
        for i in range(2)
    ]

    def setUp(self):
        super(AuctionAwardSwitch2ResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))

        response = self.app.post_json(
            '/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': self.initial_bids}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    test_switch_verification_to_unsuccessful_2 = snitch(
        switch_verification_to_unsuccessful_2)
    test_switch_active_to_unsuccessful_2 = snitch(
        switch_active_to_unsuccessful_2)


@unittest.skip("option not available")
class AuctionLotAuctionPeriodResourceTest(AuctionAuctionPeriodResourceTest):
    initial_lots = test_lots


class AuctionComplaintSwitchResourceTest(BaseAuctionWebTest):

    test_switch_to_pending = snitch(switch_to_pending)
    test_switch_to_complaint = snitch(switch_to_complaint)


@unittest.skip("option not available")
class AuctionLotComplaintSwitchResourceTest(
        AuctionComplaintSwitchResourceTest):
    initial_lots = test_lots


@unittest.skip("option not available")
class AuctionAwardComplaintSwitchResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionAwardComplaintSwitchResourceTest, self).setUp()
        # Create award
        response = self.app.post_json(
            '/auctions/{}/awards'.format(
                self.auction_id), {
                'data': {
                    'suppliers': [
                        self.initial_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']

    test_switch_to_pending_award = snitch(switch_to_pending_award)
    test_switch_to_complaint_award = snitch(switch_to_complaint_award)


@unittest.skip("option not available")
class AuctionLotAwardComplaintSwitchResourceTest(
        AuctionAwardComplaintSwitchResourceTest):
    initial_lots = test_lots

    def setUp(self):
        super(AuctionAwardComplaintSwitchResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(self.auction_id), {'data': {
            'suppliers': [self.initial_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_bids[0]['lotValues'][0]['relatedLot']
        }})
        award = response.json['data']
        self.award_id = award['id']


class AuctionDontSwitchSuspendedAuction2ResourceTest(BaseAuctionWebTest):
    initial_bids = test_bids

    test_switch_suspended_auction_to_auction = snitch(
        switch_suspended_auction_to_auction)


@unittest.skip("option not available")
class AuctionDontSwitchSuspendedAuctionResourceTest(
        BaseAuctionWebTest,
        AuctionDontSwitchSuspendedAuctionResourceTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionDontSwitchSuspendedAuctionResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": b['value']
                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json(
            '/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


class AuctionContractSwitchResourceTest(BaseAuctionWebTest,):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractSwitchResourceTest, self).setUp()
        fixtures.create_award(self)
        self.contract_id = self.award_contract_id  # use autocreated contract

    test_contract_signing_period_switch_to_complete = snitch(
        contract_signing_period_switch_to_complete
    )


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionSwitchQualificationResourceTest))
    tests.addTest(unittest.makeSuite(AuctionSwitchAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AuctionSwitchUnsuccessfulResourceTest))
    tests.addTest(unittest.makeSuite(
        AuctionLotSwitchQualificationResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotSwitchAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotSwitchUnsuccessfulResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAuctionPeriodResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAward2BidsSwitchResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAwardSwitch2ResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotAuctionPeriodResourceTest))
    tests.addTest(unittest.makeSuite(AuctionComplaintSwitchResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotComplaintSwitchResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAwardComplaintSwitchResourceTest))
    tests.addTest(unittest.makeSuite(
        AuctionLotAwardComplaintSwitchResourceTest))
    tests.addTest(unittest.makeSuite(
        AuctionDontSwitchSuspendedAuction2ResourceTest))
    tests.addTest(unittest.makeSuite(
        AuctionDontSwitchSuspendedAuctionResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
