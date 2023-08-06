import inspect

from threading import current_thread
from weakref import finalize, WeakValueDictionary, WeakKeyDictionary

from sqlalchemy.orm.scoping import (scoped_session, warn)


class SessionRope:
    def __init__(self, registry):
        self.registry = registry

    def remove(self):
        if self.registry.has():
            self.registry().close()
        self.registry.clear()

    def __del__(self):
        self.remove()

    @property
    def session(self):
        return self.registry()


class SessionJenny(scoped_session):
    def __init__(self, session_factory, scopefunc=None):
        super().__init__(session_factory, scopefunc)

        self._ropes = WeakValueDictionary()
        self._rope_name_callback = None
        self._finalizers = dict()

    def create_rope_name(self):
        if self.rope_name_callback:
            name = self.rope_name_callback()
            if not isinstance(name, str):
                raise TypeError("return value of rope_name_callback must be a str")
        return "session{}:{}".format(id(self), current_thread().ident)

    def _finalizer(self, rope_name):
        if rope_name in self._ropes:
            del self._ropes[rope_name]
        if rope_name in self._finalizers:
            del self._finalizers[rope_name]
        self.remove(rope_name)

    @property
    def rope_name_callback(self):
        return self._rope_name_callback

    @rope_name_callback.setter
    def rope_name_callback(self, fc):
        if not callable(fc):
            raise TypeError("callback must be a function")
        self._rope_name_callback = fc

    def set_rope(self, frame=None):
        if not frame:
            frame = self._outer_frame(inspect.getouterframes(inspect.currentframe()))

        rope = SessionRope(self.registry)
        self._ropes[self.create_rope_name()] = rope
        self._finalizers[self.create_rope_name()] = finalize(rope, self._finalizer, self.create_rope_name())
        frame.f_locals[self.create_rope_name()] = rope

    def _outer_frame(self, frame):
        for f in frame:
            code = f.frame.f_code
            name = code.co_name
            if name not in dir(self):
                return f.frame

    @property
    def rope(self):
        if self.create_rope_name() in self._ropes:
            rope = self._ropes[self.create_rope_name()]
            self._finalizers[self.create_rope_name()] = finalize(rope, self._finalizer, self.create_rope_name())
            return self._ropes[self.create_rope_name()]

        self.set_rope()
        return self._ropes[self.create_rope_name()]

    @property
    def session(self):
        return self.rope.session

    def remove(self, rope_name=None):
        if self.registry.has():
            self.registry().close()
        self.registry.clear()
        if not rope_name:
            rope_name = self.create_rope_name()
        try:
            del self._ropes[rope_name]
            del self._finalizers[rope_name]
        except KeyError:
            warn("There is no Session instance.")
