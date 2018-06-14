# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.swiftsure.models import (
    SwiftsureAuction,
)
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin
)


class AuctionSwiftsureConfigurator(AuctionConfigurator,
                                   AwardingV3_1ConfiguratorMixin):
    name = 'Auction Swiftsure Configurator'
    model = SwiftsureAuction


class AuctionSwiftsureManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        auction = request.validated['auction']
        for i in request.validated['json_data'].get('documents', []):
            document = type(auction).documents.model_class(i)
            document.__parent__ = auction
            auction.documents.append(document)

    def change_auction(self, request):
        pass
