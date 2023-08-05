"""
Numerical data type
"""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.unit import validate_unit, parse_unit

# Globals and constants variables.
from pyhmsa.type.unit import  _PREFIXES_VALUES

_SUPPORTED_DTYPES = frozenset(map(np.dtype, [np.uint8, np.int16, np.uint16,
                                             np.int32, np.uint32, np.int64,
                                             np.float32, np.float64]))

def validate_dtype(arg):
    if isinstance(arg, np.dtype):
        dtype = arg
    elif isinstance(arg, type) and issubclass(arg, np.generic):
        dtype = np.dtype(arg)
    elif hasattr(arg, 'dtype'):
        dtype = arg.dtype
    else:
        raise ValueError('Cannot find dtype of argument')

    if dtype not in _SUPPORTED_DTYPES:
        raise ValueError('Unsupported data type: %s' % dtype.name)

    return True

class arrayunit(np.ndarray):

    def __new__(cls, shape, dtype=np.float32, buffer=None, offset=0,
                 strides=None, order=None, unit=None):
        validate_dtype(dtype)
        obj = super().__new__(cls, shape, dtype, buffer, offset, strides, order)

        if unit is not None:
            unit = validate_unit(unit)
        obj._unit = unit

        return obj

    def __reduce__(self):
        # Solution from http://stackoverflow.com/questions/26598109/preserve-custom-attributes-when-pickling-subclass-of-numpy-array
        pickled_state = super().__reduce__()
        new_state = pickled_state[2] + (self.unit,)
        return (pickled_state[0], pickled_state[1], new_state)

    def __setstate__(self, state):
        self._unit = state[-1]
        super().__setstate__(state[0:-1])

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._unit = getattr(obj, '_unit', None)

    def __array_wrap__(self, out_arr, context=None):
        ret_arr = super().__array_wrap__(out_arr, context)
        return np.array(ret_arr) # Cast as regular array

    def __str__(self):
        if self._unit is not None:
            return super().__str__() + ' ' + self.unit
        else:
            return super().__str__()

    def __format__(self, spec):
        if not spec:
            return format(super().__str__(), spec)
        elif spec[-1].lower() in ['f', 'e', 'g', 'n']:
            return format(float(self), spec)
        elif spec[-1] in ['d']:
            return format(int(self), spec)
        else:
            return format(super().__str__(), spec)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.unit == getattr(other, 'unit', self.unit)

    def __ne__(self, other):
        return not self == other

    @property
    def unit(self):
        return self._unit

def convert_value(value, unit=None):
    if value is None:
        return None

    if not isinstance(value, arrayunit):
        value = np.asarray(value)
    else:
        unit = value.unit or unit

    return arrayunit(value.shape, value.dtype, value, unit=unit)

def convert_unit(newunit, value, oldunit=None):
    if value is None:
        return None

    if oldunit is None:
        oldunit = value.unit

    newprefix, newbaseunit, newexponent = parse_unit(newunit)
    newprefix_value = _PREFIXES_VALUES.get(newprefix, 1.0)

    oldprefix, oldbaseunit, oldexponent = parse_unit(oldunit)
    oldprefix_value = _PREFIXES_VALUES.get(oldprefix, 1.0)

    # Fix for non SI units
    if newbaseunit == 'm' and oldbaseunit == u'\u00c5':
        oldbaseunit = 'm'
        oldprefix_value *= 1e-10
    elif newbaseunit == u'\u00c5' and oldbaseunit == 'm':
        oldbaseunit = u'\u00c5'
        oldprefix_value *= 1e10

    elif newbaseunit == 'rad' and oldbaseunit == 'degrees':
        oldbaseunit = 'rad'
        oldprefix_value *= np.pi / 180.0
    elif newbaseunit == 'degrees' and oldbaseunit == 'rad':
        oldbaseunit = 'degrees'
        oldprefix_value *= 180.0 / np.pi

    # Check
    if newbaseunit != oldbaseunit:
        raise ValueError('Base units must match: %s != %s' % \
                         (newbaseunit, oldbaseunit))
    if newexponent != oldexponent:
        raise ValueError('Exponents must match: %s != %s' % \
                         (newexponent, oldexponent))

    # Conversion
    factor = oldprefix_value ** oldexponent / newprefix_value ** oldexponent
    newvalue = value * factor

    if hasattr(value, 'unit'):
        newvalue = convert_value(newvalue, newunit)

    return newvalue
