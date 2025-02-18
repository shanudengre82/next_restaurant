import io

import pandas as pd
import streamlit as st


def get_raw_data() -> pd.DataFrame:
    csv_str = st.secrets["my_secrets"]["raw_data"]
    df = pd.read_csv(io.StringIO(csv_str))
    return df
