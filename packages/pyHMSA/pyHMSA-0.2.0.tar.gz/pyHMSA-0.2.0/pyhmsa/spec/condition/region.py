"""
Region of interest condition
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.util.parameter import NumericalRangeAttribute

# Globals and constants variables.

class RegionOfInterest(_Condition):

    TEMPLATE = 'RegionOfInterest'

    channels = NumericalRangeAttribute(None, 0, required=True, doc='Channel range')

    def __init__(self, start_channel, end_channel):
        """
        Defines a region of a spectrum (or other one-dimensional datum),
        as may be useful for defining start and end channels used for a region
        of interest image.

        :arg start_channel: start channel (required)
        :arg end_channel: end channel (required)
        """
        super().__init__()

        self.channels = (start_channel, end_channel)

    def get_start_channel(self):
        """
        Returns the start channel.
        """
        return self.channels[0]

    start_channel = property(get_start_channel, doc='Start channel')

    def get_end_channel(self):
        """
        Returns the end channel.
        """
        return self.channels[1]

    end_channel = property(get_end_channel, doc='End channel')
