from textwrap import dedent


class ValidationError(Exception):
    pass


def validator(*example):
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


class Parameter(object):
    """
    Represents a generic parameter. Validates based on the provided possible
    values, e.g.::

        >>> Parameter("name", "the name to use", str).validate("asdf")
        True

        >>> Parameter("name", "the name to use", int).validate(999)
        False
    """
    def __init__(self, param, desc, values):
        self.param = param
        self.desc = " ".join(dedent(desc).splitlines(False))
        self.values = values

    def __str__(self):
        return '<%s "%s" at %s>' \
            % (self.__class__.__name__, self.param, id(self))

    def validate(self, value):

        if isinstance(self.values, set):
            if value in self.values:
                return True

        if isinstance(self.values, type):
            if isinstance(value, self.values):
                return True
            return False

        if hasattr(self.values, '__call__'):
            return self.values(value)

        elif value == self.values:
            return True


@validator("tag=value")
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
    if isinstance(v, basestring):
        return True


@validator("a:b:c")
def ColSV3(v):
    nvalues = 3
    if not isinstance(v, basestring):
        raise ValueError('not a string')
    vs = v.split(':')
    assert len(vs) == nvalues
    return True


@validator("a:b")
def ColSV2(v):
    nvalues = 2
    if not isinstance(v, basestring):
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
    assert isinstance(v, basestring), "RGB tuple is not a string"
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
