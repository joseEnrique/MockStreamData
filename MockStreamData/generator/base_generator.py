from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    def __aiter__(self):
        """Return the async iterator (self)."""
        return self

    @abstractmethod
    async def __anext__(self):
        """Return the next item asynchronously."""
        pass
