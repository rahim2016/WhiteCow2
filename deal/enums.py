from enum import Enum


class TimeInterval(Enum):
    one_min = '1 min'
    every_day = '7 days'
    week_ends = '2 days'


class SetupStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'