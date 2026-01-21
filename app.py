import streamlit as st
import tempfile
import os
import json

from executable import process_image
from extraction.dealer_name import load_dealers
from extraction.model_name import load_models

st.set_page_config(page_title="Intelligent Invoice Parser", layout="wide")

st.title(" Intelligent Invoice Parser")
st.caption("Upload an invoice image to extract structured data")

# Load masters once
dealers = load_dealers("data/master/dealer_master.csv")
models = load_models("data/master/model_master.txt")

uploaded_files = st.file_uploader(
    "Upload invoice images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    results = []

    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        result = process_image(tmp_path, dealers, models)
        results.append(result)

        st.subheader(f" {file.name}")
        st.json(result)

    st.subheader(" Combined Output")
    st.json(results)
