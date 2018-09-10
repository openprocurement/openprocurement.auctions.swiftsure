# -*- coding: utf-8 -*-

VIEW_LOCATIONS = [
    "openprocurement.auctions.swiftsure.views",
]

DEFAULT_PROCUREMENT_METHOD_TYPE = "Swiftsure"
CONTRACT_TYPES = ['yoke']
DEFAULT_LEVEL_OF_ACCREDITATION = {'create': [3],
                                  'edit': [4]}
SWIFTSURE_STATUSES = (
    'draft',
    'pending.activation',
    'active.tendering',
    'active.auction',
    'active.qualification',
    'active.awarded',
    # 'pending.complete',
    # 'pending.cancelled',
    # 'pending.unsuccessful',
    'complete',
    'cancelled',
    'unsuccessful',
)

SWIFTSURE_PRE_TERMINAL_STATUSES = (
    'pending.complete',
    'pending.cancelled',
    'pending.unsuccessful',
)

SWIFTSURE_TERMINAL_STATUSES = (
    'complete',
    'cancelled',
    'unsuccessful',
)
SWIFTSURE_DEFAULT_STATUS = 'active.tendering'
