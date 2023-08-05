"""
X-ray line type
"""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
NOTATION_IUPAC = 'IUPAC'
NOTATION_SIEGBAHN = 'Siegbahn'

_NOTATIONS = frozenset([NOTATION_IUPAC, NOTATION_SIEGBAHN])

class xrayline(str):

    def __new__(cls, value, notation, altvalue=None):
        # Preference over ASCII characters over Unicode characters
        value = value.replace(u"\u03b1", 'a')
        value = value.replace(u"\u03b2", 'b')
        value = value.replace(u"\u03b3", 'g')
        value = value.replace(u"\u03b6", 'z')
        value = value.replace(u"\u03b7", 'n')

        obj = super().__new__(cls, value)

        if notation not in _NOTATIONS:
            raise ValueError("Unknown x-ray line notation: %s" % notation)
        obj._notation = notation

        if altvalue is not None:
            altnotation = next(iter(_NOTATIONS - set([notation])))
            altvalue = xrayline(altvalue, altnotation)
        obj._alternative = altvalue

        return obj

    def __reduce__(self):
        return (self.__class__,
                (str(self), self.notation, str(self.alternative)))

    @property
    def notation(self):
        return self._notation

    @property
    def alternative(self):
        return self._alternative

