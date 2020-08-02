from __future__ import absolute_import
import os
import warnings
import tempfile
from collections import OrderedDict


def deprecation_handler(source, filename, kwargs):
    if 'local_fn' in kwargs:
        warnings.warn(
            'Please use the argument "source" instead of "local_fn"',
            DeprecationWarning)
        if source is not None:
            raise ValueError(
                'Both "source" and "local_fn" are specified. Please use '
                'just "source"')
        source = kwargs.pop('local_fn')

    if 'remote_fn' in kwargs:
        warnings.warn(
            'Please use the argument "source" instead of "remote_fn"',
            DeprecationWarning)
        if filename is not None:
            raise ValueError(
                'Both "filename" and "remote_fn" are specified. Please use '
                'just "filename"')
        filename = kwargs.pop('remote_fn')
    return source, filename


class HubComponent(object):
    """
    Base class for various track hub components.  Several methods must be
    overridden by subclasses.
    """
    def __init__(self):
        self.children = []
        self.parent = None

    def _render(self, staging='staging'):
        """
        Renders the object to file.  Must be overridden by subclass.

        Can return None if nothing to be done for the subclass.
        """
        raise NotImplementedError(
            "%s: subclasses must define their own _render() method"
            % self.__class__.__name__)

    def validate(self):
        """
        Runs validation, raising exceptions as needed.  Must be overridden by
        subclass.
        """
        raise NotImplementedError(
            "%s: subclasses must define their own validate() method"
            % self.__class__.__name__)

    def add_child(self, child):
        """
        Adds self as parent to child, and then adds child.
        """
        child.parent = self
        self.children.append(child)
        return child

    def add_parent(self, parent):
        """
        Adds self as child of parent, then adds parent.
        """
        parent.add_child(self)
        self.parent = parent
        return parent

    def root(self, cls=None, level=0):
        """
        Returns the top-most HubComponent in the hierarchy.

        If `cls` is not None, then return the top-most attribute HubComponent
        that is an instance of class `cls`.

        For a fully-constructed track hub (and `cls=None`), this should return
        a a Hub object for every component in the hierarchy.
        """
        if cls is None:
            if self.parent is None:
                return self, level
        else:
            if isinstance(self, cls):
                if not isinstance(self.parent, cls):
                    return self, level

        if self.parent is None:
            return None, None

        return self.parent.root(cls, level - 1)

    def leaves(self, cls, level=0, intermediate=False):
        """
        Returns an iterator of the HubComponent leaves that are of class `cls`.

        If `intermediate` is True, then return any intermediate classes as
        well.
        """
        if intermediate:
            if isinstance(self, cls):
                yield self, level
        elif len(self.children) == 0:
            if isinstance(self, cls):
                yield self, level
            else:
                raise StopIteration

        for child in self.children:
            for leaf, _level in child.leaves(
                cls, level + 1, intermediate=intermediate
            ):
                    yield leaf, _level

    def render(self, staging=None):
        """
        Renders the object to file, returning a list of created files.

        Calls validation code, and, as long as each child is also a subclass of
        :class:`HubComponent`, the rendering is recursive.
        """
        self.validate()
        created_files = OrderedDict()
        if staging is None:
            staging = tempfile.mkdtemp()
        this = self._render(staging)
        if this:
            created_files[repr(self)] = this
        for child in self.children:
            created_files[repr(child)] = child.render(staging)
        return created_files

    def makedirs(self, fn):
        dirname = os.path.dirname(fn)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
