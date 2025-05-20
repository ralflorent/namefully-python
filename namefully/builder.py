from collections import deque
from typing import Callable, Generic, Iterable, Optional, TypeVar

from ._name import Name
from ._namefully import Namefully
from ._validators import SequentialNameValidator

T = TypeVar('T')
I = TypeVar('I')


class Builder(Generic[T, I]):
    """A generic builder base class."""

    def __init__(
        self,
        prebuild: Optional[Callable[[], None]] = None,
        postbuild: Optional[Callable[[I], None]] = None,
        preclear: Optional[Callable[[I], None]] = None,
        postclear: Optional[Callable[[], None]] = None,
    ):
        """Initialize the builder with optional lifecycle hooks."""
        self.prebuild = prebuild
        self.postbuild = postbuild
        self.preclear = preclear
        self.postclear = postclear
        self._queue: deque[T] = deque()
        self._instance: Optional[I] = None

    @property
    def size(self) -> int:
        """Get the current size of the builder."""
        return len(self._queue)

    def remove_first(self) -> Optional[T]:
        """Remove and return the first element of the queue."""
        return self._queue.popleft() if self._queue else None

    def remove_last(self) -> Optional[T]:
        """Remove and return the last element of the queue."""
        return self._queue.pop() if self._queue else None

    def add_first(self, value: T) -> None:
        """Add value at the beginning of the queue."""
        self._queue.appendleft(value)

    def add_last(self, value: T) -> None:
        """Add value at the end of the queue."""
        self._queue.append(value)

    def add(self, *values: T) -> None:
        """Add values at the end of the queue."""
        self._queue.extend(values)

    def remove(self, value: T) -> bool:
        """Remove a single instance of value from the queue."""
        try:
            self._queue.remove(value)
            return True
        except ValueError:
            return False

    def remove_where(self, callable: Callable[[T], bool]) -> None:
        """Remove all elements matched by callable from the queue."""
        self._queue = deque(x for x in self._queue if not callable(x))

    def retain_where(self, callable: Callable[[T], bool]) -> None:
        """Remove all elements not matched by callable from the queue."""
        self._queue = deque(x for x in self._queue if callable(x))

    def clear(self) -> None:
        """Remove all elements in the queue."""
        if self._instance is not None and self.preclear:
            self.preclear(self._instance)
        self._queue.clear()
        if self.postclear:
            self.postclear()
        self._instance = None

    def build(self) -> I:
        """Build the desired instance."""
        raise NotImplementedError('Subclasses must implement build()')


class NameBuilder(Builder[Name, Namefully]):
    """An on-the-fly name builder.

    The builder uses a lazy-building method while capturing all necessary Names
    to finally construct a complete Namefully instance.

    Example:
        builder = NameBuilder.of([Name.first('Thomas'), Name.last('Edison')])
        builder.add(Name.middle('Alva'))
        print(builder.build())  # 'Thomas Alva Edison'
    """

    def __init__(
        self,
        name: Optional[Name] = None,
        prebuild: Optional[Callable[[], None]] = None,
        postbuild: Optional[Callable[[Namefully], None]] = None,
        preclear: Optional[Callable[[Namefully], None]] = None,
        postclear: Optional[Callable[[], None]] = None,
    ):
        """Initialize the name builder with an optional initial name."""
        super().__init__(prebuild, postbuild, preclear, postclear)
        if name is not None:
            self.add(name)

    @classmethod
    def of(cls, *initial_names: Name) -> 'NameBuilder':
        """Create a base builder from many Names to construct Namefully later."""
        builder = cls()
        builder.add(*initial_names)
        return builder

    @classmethod
    def use(
        cls,
        names: Optional[Iterable[Name]] = None,
        prebuild: Optional[Callable[[], None]] = None,
        postbuild: Optional[Callable[[Namefully], None]] = None,
        preclear: Optional[Callable[[Namefully], None]] = None,
        postclear: Optional[Callable[[], None]] = None,
    ) -> 'NameBuilder':
        """Create a base builder from many Names with lifecycle hooks."""
        builder = cls(prebuild=prebuild, postbuild=postbuild, preclear=preclear, postclear=postclear)
        if names:
            builder.add(*names)
        return builder

    def build(
        self,
        *,
        context: Optional[str] = None,
        ordered_by: str = 'first_name',
        separator: str = ' ',
        title: str = 'uk',
        ending: bool = False,
        bypass: bool = True,
        surname: str = 'father',
    ) -> Namefully:
        """Build an instance of Namefully from the previously collected names.

        Regardless of how the names are added, both first and last names must exist
        to complete a fine build. Otherwise, it throws a NameError.
        """
        if self.prebuild:
            self.prebuild()

        names = list(self._queue)
        SequentialNameValidator().validate_as_name(names)

        self._instance = Namefully(
            names,
            context=context,
            ordered_by=ordered_by,
            separator=separator,
            title=title,
            ending=ending,
            bypass=bypass,
            surname=surname,
        )

        if self.postbuild:
            self.postbuild(self._instance)

        return self._instance
