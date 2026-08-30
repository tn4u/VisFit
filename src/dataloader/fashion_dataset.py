"""Dataset placeholders for fashion recommendation experiments.

This module defines placeholder PyTorch dataset classes for fashion datasets used by
VisFit, including FashionIQ triplets and Polyvore disjoint training data.
"""

from __future__ import annotations

from typing import Any, Tuple


class FashionIQTripletDataset:
    """Placeholder dataset for FashionIQ triplet-style training data."""

    def __init__(self, data_root: str, transform: Any | None = None) -> None:
        self.data_root = data_root
        self.transform = transform

    def __len__(self) -> int:
        """Return the dataset size."""
        return 0

    def __getitem__(self, idx: int) -> Tuple[Any, Any, Any]:
        """Return a placeholder sample: reference image, target image, text pair."""
        raise NotImplementedError("Implement FashionIQ triplet loading logic here.")


class PolyvoreDisjointDataset:
    """Placeholder dataset for Polyvore disjoint outfit recommendation data."""

    def __init__(self, data_root: str, transform: Any | None = None) -> None:
        self.data_root = data_root
        self.transform = transform

    def __len__(self) -> int:
        """Return the dataset size."""
        return 0

    def __getitem__(self, idx: int) -> Tuple[Any, Any, Any]:
        """Return a placeholder sample for outfit-based recommendation."""
        raise NotImplementedError("Implement Polyvore disjoint dataset loading logic here.")
