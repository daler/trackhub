from textwrap import dedent
from .compatibility import string_types


class ValidationError(Exception):
    pass


def validator(*example):
    """
    Decorator that runs a self-test on the validator it decorates
    """
    def wrapper(func):

        # Try running validation on the function's own example . . . it better
        # work!
        example_string = []
        try:
                for ex in example:
                    func(ex)
                    example_string.append(ex)
                example_string = 'Example value(s): %s' \
                    % (" or ".join('%r' % i for i in example_string))

        except Exception as e:
            raise ValueError(
                'Error validating example (func=%s, example=%r)! '
                '\nOriginal error:\n\t%s: %s'
                % (func.func_name, example, e.__class__.__name__, e.message))

        class Validator(object):
            """
            Class to wrap a function and display an example value.
            """
            def __call__(self, v):
                try:
                    return func(v)
                except Exception as e:
                    raise ValidationError(
                        '%s; %s'
                        % (e.message, example_string))

            def __str__(self):
                return "<Validator [%s] at %s> sample: %s" \
                    % (func.func_name, id(func), example)

        return Validator()
    return wrapper


class Param(object):
    def __init__(self, name, fmt, types, required, validator, min_bed_fields=None):
        """
        Parameters
        ----------

        name : str
            Name of the parameter

        fmt : list
            List of strings parsed from the "format" section of the spec from
            UCSC. Mostly used as an informal guide to the format.

        types : list
            List of track types this parameter applies to

        required : bool or list
            If True, all tracks must have it. If list, only those types must
            have it.

        validator : callable, set, or type
            Validation to run on user-provided values. If callable, must return
            True if the value passes. If set, validation will pass if the value
            is in the provided set.

        min_bed_fields : int
            Some parameters only work for a certain number of BED fields. Specify that here.

        Examples
        --------

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate(999)
        True

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate('999')
        True

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate(0)
        """
        self.name = name
        self.fmt = fmt
        self.types = types
        self.required = required
        self.validator = validator

    def __str__(self):
        return '<%s "%s" at %s>' \
            % (self.__class__.__name__, self.name, id(self))

    def validate(self, value):

        if isinstance(self.validator, set):
            if value in self.validator:
                return True

        if isinstance(self.validator, type):
            if isinstance(value, self.validator):
                return True
            else:
                # Otherwise, allow any exceptions to propagate up.
                self.validator(value)
                return True

        if hasattr(self.validator, '__call__'):
            return self.validator(value)

        elif value == self.validator:
            return True

@validator("tag=value", "tag1=val1 tag2=val2")
def key_val(v):
    try:
        assert '=' in v
        items = v.split()
        assert len(items) == v.count('=')
        return True

    except AssertionError:
        return False


@validator("a,b,c")
def CSV(v):
    #TODO: is a one-item list "chr1," or "chr1"?
    if isinstance(v, string_types):
        return True


@validator("a:b:c")
def ColSV3(v):
    nvalues = 3
    if not isinstance(v, string_types):
        raise ValueError('not a string')
    vs = v.split(':')
    assert len(vs) == nvalues
    return True


@validator("a:b")
def ColSV2(v):
    nvalues = 2
    if not isinstance(v, string_types):
        raise ValueError('not a string')
    vs = v.split(':')
    assert len(vs) == nvalues
    return True


@validator("128,0,255")
def RGB(v):
    if ' ' in v:
        raise ValueError('Space in RGB tuple')
    if "." in v:
        raise ValueError('"." in RGB tuple')
    assert isinstance(v, string_types), "RGB tuple is not a string"
    if ',' not in v:
        raise ValueError("no commas in RGB tuple")
    rgb = v.split(',')
    assert len(rgb) == 3, "RGB tuple does not have 3 values"
    try:
        rgb = map(int, rgb)
    except ValueError:
        raise ValueError('RGB tuple does not contain ints')
    for i in rgb:
        assert (0 <= i <= 255)
    return True


@validator("128,0,0 90,90,5")
def RGBList(v):
    rgbs = v.split(' ')
    assert len(rgbs) == 2, "RGBList not a space-separated list of RGB tuples"
    for i in rgbs:
        RGB(i)
    return True


@validator("off", 1)
def off_or_int(v):
    try:
        int(v)
        return True
    except ValueError:
        if v == 'off':
            return True
        raise

@validator("chr21:33031596-33033258")
def ucsc_position(v):
    try:
        chrom, pos = v.split(":")
        start, end = pos.split("-")
        start = int(start)
        end = int(end)
    except ValueError:
        raise ValueError("UCSC position string is formatted incorrectly")
    assert start >= 0, "start position must be a positive integer"
    assert end >= 0, "end position must be a positive integer"
    assert start < end, "start must be less than end"
    return True
