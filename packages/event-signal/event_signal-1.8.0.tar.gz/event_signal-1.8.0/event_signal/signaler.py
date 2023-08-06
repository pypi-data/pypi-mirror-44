from .interface import SignalerInstance, SignalerDescriptorInstance, copy_signals_as_bound
from .signaler_prop import signaler_property


__all__ = ["signaler", "SignalerDecoratorInstance"]


class SignalerDecoratorInstance(SignalerDescriptorInstance):
    def __init__(self, func=None, getter=None, fire_results=False):
        """Decorate a function to emit signals.

        Args:
            func (callable)[None]: Callable function that you want to decorate.
            getter (callable)[None]: Takes no arguments and returns a single argument that is used when firing
                the change signal.
        """
        self._func = None

        super(SignalerDecoratorInstance, self).__init__()

        self.func = func
        self.getter = getter
        self.fire_results = fire_results
        self.event_signals["before_change"] = []
        self.event_signals["change"] = []

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func):
        self._func = func

    def _update_func(self):
        try:
            self.__module__ = self._func.__module__
        except AttributeError:
            pass
        try:
            self.__name__ = self._func.__name__
        except AttributeError:
            pass
        try:
            self.__qualname__ = self._func.__qualname__
        except AttributeError:
            pass
        try:
            self.__doc__ = self._func.__doc__
        except AttributeError:
            pass
        try:
            self.__annotations__ = self._func.__annotations__
        except AttributeError:
            pass

    def __call__(self, *args, **kwargs):
        if self.func is None and callable(args[0]):
            # Decorating a function
            self.func = args[0]
            return self
        else:
            # Calling this class
            self.fire("before_change", *args, **kwargs)
            ret = self.func(*args, **kwargs)

            if self.getter is None:
                if self.fire_results:
                    self.fire("change", ret)
                else:
                    self.fire("change", *args, **kwargs)
            else:
                self.fire("change", self.getter())
            return ret

    def create_signaler_instance(self, instance=None):
        """Create and return a signaler instance."""
        pass


class signaler(SignalerDecoratorInstance):
    """Signaler used with binded methods and instances. Does not allow using as a decorator."""

    property = signaler_property

    def create_signaler_instance(self, instance=None):
        """Create and return a signaler instance."""
        func = None
        getter = None
        if self.func:
            func = self.func.__get__(instance, instance.__class__)
        if self.getter:
            getter = self.getter.__get__(instance, instance.__class__)

        # Create the new signaler for the instance with bound methods.
        sig = SignalerDecoratorInstance(func, getter=getter, fire_results=self.fire_results)

        # Map all of the connected callbacks as bound methods to the instance
        copy_signals_as_bound(self, sig, instance)

        return sig  # return an event handler object for the instance

    def __get__(self, instance, owner):
        """Return the signaler with a binded method callback."""
        return self.get_signaler_instance(instance)
