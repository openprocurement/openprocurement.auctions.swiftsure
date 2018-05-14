import logging

from pyramid.interfaces import IRequest
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.swiftsure.models import (
    ISwiftsureAuction,
    SwiftsureAuction,
)
from openprocurement.auctions.swiftsure.adapters import (
    AuctionSwiftsureConfigurator,
    AuctionSwiftsureManagerAdapter
)
from openprocurement.auctions.core.plugins.awarding.v3.adapters import (
    AwardingNextCheckV3
)
from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    IAwardingNextCheck
)
from openprocurement.auctions.swiftsure.constants import (
    VIEW_LOCATIONS,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    procurement_method_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(SwiftsureAuction,
                                                 procurementMethodType)

    for view_location in VIEW_LOCATIONS:
        config.scan(view_location)

    # Register adapters
    config.registry.registerAdapter(
        AuctionSwiftsureConfigurator,
        (ISwiftsureAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AuctionSwiftsureManagerAdapter,
        (ISwiftsureAuction,),
        IAuctionManager
    )
    config.registry.registerAdapter(
        AwardingNextCheckV3,
        (ISwiftsureAuction,),
        IAwardingNextCheck
    )

    LOGGER.info("Included openprocurement.auctions.swiftsure plugin",
                extra={'MESSAGE_ID': 'included_plugin'})
