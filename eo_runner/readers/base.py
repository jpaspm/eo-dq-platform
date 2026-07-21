"""
Reader Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from eo_core.models import DatasetDescriptor


class BaseReader(ABC):

    @abstractmethod
    def discover(self) -> Iterable[DatasetDescriptor]:
        """
        Discover available datasets.

        Returns
        -------
        Iterable[DatasetDescriptor]
        """
        raise NotImplementedError

    @abstractmethod
    def read(self, dataset: DatasetDescriptor):
        """
        Read all records from a dataset.

        Parameters
        ----------
        dataset
            Dataset descriptor returned by discover().
        """
        raise NotImplementedError