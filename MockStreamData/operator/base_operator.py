from abc import ABC, abstractmethod


# --- Base interface for operators ---
class BaseOperator(ABC):
    @abstractmethod
    async def start(self):
        """Initialize the operator."""
        pass

    @abstractmethod
    async def send(self, data):
        """Send data using the operator."""
        pass

    @abstractmethod
    async def stop(self):
        """Close or release the operator's resources."""
        pass