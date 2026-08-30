"""Minimal Streamlit application for the VisFit project."""

from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="VisFit", page_icon="👗")

st.title("VisFit")
st.write(
    "A computer vision and fashion recommendation system for outfit matching and image-based retrieval."
)

uploaded_file = st.file_uploader("Upload a fashion image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded fashion image", use_container_width=True)

st.subheader("Outfit Recommendation")
st.write("Placeholder for outfit recommendation results.")

st.subheader("Similarity Search")
st.write("Placeholder for nearest-neighbor or embedding-based similarity search.")
