from pathlib import Path

import streamlit as st
import torch
from PIL import Image

from src.models.branch_a_model import (
    BranchAModel
)

from src.retrievals.branch_a_retrieval import (
    BranchARetriever
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="VisFit",
    page_icon="👕",
    layout="wide"
)


# =========================================================
# PATH CONFIG
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "models"
    / "a"
    / "best_fashionclip_inshop.pt"
)

INDEX_PATH = (
    PROJECT_ROOT
    / "indexes"
    / "inshop"
    / "gallery.index"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "metadata"
    / "inshop.csv"
)


# =========================================================
# LOAD RESOURCES
# =========================================================

@st.cache_resource
def load_resources():
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = BranchAModel(
        checkpoint_path=CHECKPOINT_PATH,
        device=device
    )

    retriever = BranchARetriever(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH
    )

    return (
        model,
        retriever,
        device
    )


try:
    model, retriever, device = (
        load_resources()
    )

except Exception as error:
    st.error(
        f"Không thể load hệ thống: {error}"
    )
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title(
    "VisFit - Fashion Image Retrieval"
)

st.caption(
    "Fine-tuned Fashion-CLIP + FAISS"
)

st.write(
    f"Device: `{device}`"
)

st.write(
    f"Gallery size: "
    f"`{retriever.index.ntotal:,}` images"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header(
        "Search Settings"
    )

    top_k = st.selectbox(
        "Top-K",
        options=[
            5,
            10,
            20
        ],
        index=1
    )


# =========================================================
# UPLOAD QUERY
# =========================================================

uploaded_file = st.file_uploader(
    "Upload một ảnh thời trang",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)


if uploaded_file is None:
    st.info(
        "Hãy upload một ảnh để bắt đầu tìm kiếm."
    )
    st.stop()


query_image = Image.open(
    uploaded_file
).convert("RGB")


# =========================================================
# DISPLAY QUERY
# =========================================================

st.subheader(
    "Query Image"
)

query_col, info_col = st.columns(
    [1, 2]
)

with query_col:
    st.image(
        query_image,
        use_container_width=True
    )

with info_col:
    st.write(
        f"Image size: "
        f"`{query_image.width} × {query_image.height}`"
    )

    st.write(
        "Model: "
        "`Fine-tuned Fashion-CLIP`"
    )

    st.write(
        "Embedding dimension: "
        "`512`"
    )

    st.write(
        "Similarity: "
        "`Cosine / FAISS IndexFlatIP`"
    )


# =========================================================
# SEARCH BUTTON
# =========================================================

search_clicked = st.button(
    "Search Similar Fashion",
    type="primary"
)


if search_clicked:

    with st.spinner(
        "Đang trích xuất đặc trưng và tìm kiếm..."
    ):

        query_embedding = (
            model.encode_image(
                query_image
            )
        )

        results = (
            retriever.search(
                query_embedding,
                top_k=top_k
            )
        )


    # =====================================================
    # RESULTS
    # =====================================================

    st.success(
        f"Tìm thấy Top-{len(results)} kết quả."
    )

    st.subheader(
        f"Top-{top_k} Similar Results"
    )

    columns_per_row = 5

    for start in range(
        0,
        len(results),
        columns_per_row
    ):
        cols = st.columns(
            columns_per_row
        )

        batch = results[
            start:
            start + columns_per_row
        ]

        for col, result in zip(
            cols,
            batch
        ):
            with col:

                image_path = Path(
                    result[
                        "image_path"
                    ]
                )

                if image_path.exists():

                    try:
                        result_image = Image.open(
                            image_path
                        ).convert("RGB")

                        st.image(
                            result_image,
                            use_container_width=True
                        )

                    except Exception as error:
                        st.warning(
                            f"Không đọc được ảnh: {error}"
                        )

                else:
                    st.warning(
                        "Không tìm thấy ảnh local."
                    )

                st.markdown(
                    f"**#{result['rank']}**"
                )

                st.write(
                    f"Score: "
                    f"`{result['score']:.4f}`"
                )

                st.caption(
                    f"Item: "
                    f"{result['item_id']}"
                )

                with st.expander(
                    "Chi tiết"
                ):
                    st.write(
                        "Image name:"
                    )

                    st.code(
                        result[
                            "image_name"
                        ]
                    )

                    st.write(
                        "Local path:"
                    )

                    st.code(
                        result[
                            "image_path"
                        ]
                    )