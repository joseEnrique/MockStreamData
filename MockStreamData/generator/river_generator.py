import asyncio

from MockStreamData.generator.base_generator import BaseGenerator


class RiverDatasetGenerator(BaseGenerator):
    def __init__(self, dataset, operator, stream_period=0, item_per_iter=10, n_instances=None):
        """
        :param dataset: The dataset (an iterable) to be streamed (e.g., datasets.Phishing()).
        :param operator: An optional operator (e.g., KafkaOperator). If None, the generator only produces data.
        :param stream_period: Time (in seconds) between each batch generation.
        :param item_per_iter: Number of items per batch.
        :param n_instances: Total number of batches to generate. If None, the generator runs until the dataset is exhausted.
        """
        self.dataset = dataset
        self.dataset_iter = iter(dataset)
        self.operator = operator
        self.stream_period = stream_period
        self.item_per_iter = item_per_iter
        self.n_instances = n_instances  # If provided, limit the number of batches.
        self.i = 0
        self.started = False

    async def __anext__(self):
        # Lazily initialize the operator on the first iteration, if one is provided.
        if self.operator is not None and not self.started:
            await self.operator.start()
            self.started = True

        # Stop if n_instances is provided and reached.
        if self.n_instances is not None and self.i >= self.n_instances:
            if self.operator is not None:
                await self.operator.stop()
            raise StopAsyncIteration

        # Build a batch by collecting up to 'item_per_iter' items from the dataset iterator.
        batch = []
        for j in range(self.item_per_iter):
            try:
                # Get the next data sample from the River dataset.
                item = next(self.dataset_iter)
            except StopIteration:
                # End of dataset reached.
                break
            batch.append(item)

        # If no data was collected, end the iteration.
        if not batch:
            if self.operator is not None:
                await self.operator.stop()
            raise StopAsyncIteration

        # If an operator is provided, send the batch.
        if self.operator is not None:
            await self.operator.send(batch)
            print(f"Sent batch {self.i + 1}")
        else:
            print(f"Generated batch {self.i + 1} (no operator)")

        self.i += 1
        # Wait without blocking the event loop.
        await asyncio.sleep(self.stream_period)
        return batch