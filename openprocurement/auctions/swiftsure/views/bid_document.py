# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionBidDocumentResource


@opresource(name='swiftsure:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="swiftsure",
            description="Auction bidder documents")
class AuctionBidDocumentResource(AuctionBidDocumentResource):
    pass
