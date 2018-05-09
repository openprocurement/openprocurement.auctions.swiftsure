# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import AuctionConfigurator
from openprocurement.auctions.swiftsure.models import (
    SwiftsureAuction,
)
from openprocurement.auctions.core.plugins.awarding.v3.adapters import (
    AwardingV3ConfiguratorMixin
)


class AuctionSwiftsureConfigurator(AuctionConfigurator,
                                   AwardingV3ConfiguratorMixin):
    name = 'Auction Swiftsure Configurator'
    model = SwiftsureAuction
