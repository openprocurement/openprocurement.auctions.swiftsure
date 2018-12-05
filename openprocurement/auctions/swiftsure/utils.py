# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution

from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.plugins.contracting.base.utils import (
    check_auction_status
)
from openprocurement.auctions.core.utils import (
    cleanup_bids_for_cancelled_lots, check_complaint_status,
    remove_draft_bids,
    context_unpack,
    get_now,
    TZ,
)


PKG = get_distribution(__package__)
LOGGER = getLogger(PKG.project_name)


def check_bids(request):
    auction = request.validated['auction']
    adapter = request.registry.getAdapter(auction, IAuctionManager)
    if auction.lots:
        [
            setattr(i.auctionPeriod, 'startDate', None)
            for i in auction.lots
            if i.numberOfBids < 2
            and i.auctionPeriod
            and i.auctionPeriod.startDate
        ]
        [setattr(i, 'status', 'unsuccessful') for i in auction.lots if i.numberOfBids < 2 and i.status == 'active']
        cleanup_bids_for_cancelled_lots(auction)
        if not set([i.status for i in auction.lots]).difference(set(['unsuccessful', 'cancelled'])):
            adapter.pendify_auction_status('unsuccessful')
    else:
        if auction.auctionPeriod:
            if auction.numberOfBids < auction.minNumberOfQualifiedBids:
                auction.auctionPeriod.startDate = None
                adapter.pendify_auction_status('unsuccessful')
            elif auction.numberOfBids == 1:
                auction.auctionPeriod.startDate = None
                request.content_configurator.start_awarding()


def check_status(request):
    auction = request.validated['auction']
    now = get_now()
    for complaint in auction.complaints:
        check_complaint_status(request, complaint, now)
    for award in auction.awards:
        request.content_configurator.check_award_status(request, award, now)
        for complaint in award.complaints:
            check_complaint_status(request, complaint, now)
    if not auction.lots and auction.status == 'active.tendering' and auction.tenderPeriod.endDate <= now:
        auction.status = 'active.auction'
        remove_draft_bids(request)
        check_bids(request)
        msg = 'Switched auction {} to {}'.format(auction.id, auction.status)
        context_msg = {'MESSAGE_ID': 'switched_auction_{}'.format(auction.status)}
        LOGGER.info(msg, extra=context_unpack(request, context_msg))
        return True
    elif auction.lots and auction.status == 'active.tendering' and auction.tenderPeriod.endDate <= now:
        auction.status = 'active.auction'
        remove_draft_bids(request)
        check_bids(request)
        [setattr(i.auctionPeriod, 'startDate', None) for i in auction.lots if i.numberOfBids < 2 and i.auctionPeriod]
        msg = 'Switched auction {} to {}'.format(auction.id, auction.status)
        context_msg = {'MESSAGE_ID': 'switched_auction_{}'.format(auction.status)}
        LOGGER.info(msg, extra=context_unpack(request, context_msg))
        return True
    elif not auction.lots and auction.status == 'active.awarded':
        standStillEnds = [
            a.complaintPeriod.endDate.astimezone(TZ)
            for a in auction.awards
            if a.complaintPeriod.endDate
        ]
        if not standStillEnds:
            return True
        standStillEnd = max(standStillEnds)
        if standStillEnd <= now:
            check_auction_status(request)
    elif auction.lots and auction.status in ['active.qualification', 'active.awarded']:
        if any([i['status'] in auction.block_complaint_status and i.relatedLot is None for i in auction.complaints]):
            return True
        for lot in auction.lots:
            if lot['status'] != 'active':
                continue
            lot_awards = [i for i in auction.awards if i.lotID == lot.id]
            standStillEnds = [
                a.complaintPeriod.endDate.astimezone(TZ)
                for a in lot_awards
                if a.complaintPeriod.endDate
            ]
            if not standStillEnds:
                continue
            standStillEnd = max(standStillEnds)
            if standStillEnd <= now:
                check_auction_status(request)
                return True
