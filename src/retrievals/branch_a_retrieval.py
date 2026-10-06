from pathlib import Path

import faiss
import numpy as np
import pandas as pd


class BranchARetriever:
    def __init__(
        self,
        index_path: str | Path,
        metadata_path: str | Path
    ):
        self.index_path = Path(
            index_path
        )

        self.metadata_path = Path(
            metadata_path
        )

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy FAISS index: {self.index_path}"
            )

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy metadata: {self.metadata_path}"
            )

        self.index = faiss.read_index(
            str(self.index_path)
        )

        self.metadata = pd.read_csv(
            self.metadata_path
        )

        if (
            self.index.ntotal
            != len(self.metadata)
        ):
            raise ValueError(
                "Số vector trong FAISS index "
                "không khớp số dòng metadata. "
                f"FAISS={self.index.ntotal}, "
                f"metadata={len(self.metadata)}"
            )

        required_columns = [
            "image_name",
            "item_id",
            "image_path"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in self.metadata.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Metadata thiếu columns: {missing_columns}"
            )

    def search(
        self,
        query_embedding,
        top_k=10
    ):
        query_embedding = np.ascontiguousarray(
            query_embedding,
            dtype=np.float32
        )

        if query_embedding.ndim == 1:
            query_embedding = (
                query_embedding.reshape(
                    1,
                    -1
                )
            )

        if (
            query_embedding.shape[1]
            != self.index.d
        ):
            raise ValueError(
                f"Query embedding dim="
                f"{query_embedding.shape[1]}, "
                f"FAISS dim={self.index.d}"
            )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for rank, (
            index,
            score
        ) in enumerate(
            zip(
                indices[0],
                scores[0]
            ),
            start=1
        ):
            index = int(index)

            if index < 0:
                continue

            row = self.metadata.iloc[
                index
            ]

            results.append({
                "rank": rank,
                "index": index,
                "score": float(score),
                "image_name": str(
                    row["image_name"]
                ),
                "item_id": str(
                    row["item_id"]
                ),
                "image_path": str(
                    row["image_path"]
                )
            })

        return results