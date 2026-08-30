"""Evaluation metrics for recommendation quality.

This module contains placeholder implementations for Recall@K and NDCG@K.
"""

from __future__ import annotations


def recall_at_k(relevances, k: int = 10) -> float:
    """Compute Recall@K for a ranked recommendation list."""
    raise NotImplementedError("Implement Recall@K calculation here.")


def ndcg_at_k(relevances, k: int = 10) -> float:
    """Compute NDCG@K for a ranked recommendation list."""
    raise NotImplementedError("Implement NDCG@K calculation here.")
