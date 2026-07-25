import pandas as pd
import re

def clean_property_tokens(df):
    """
    Cleans and normalizes property type strings into standardized lists/tokens.
    (Paste the exact logic from your training notebook/script here)
    """
    # Replace this placeholder with the exact body of your clean_property_tokens function
    df = df.copy()
    if "Primary Property Types" in df.columns:
        df["Primary Property Types"] = df["Primary Property Types"].apply(
            lambda x: [item.strip().lower() for item in str(x).split(",")] if pd.notna(x) else []
        )
    return df


def engineer_domain_features(df):
    """
    Engineers spatial and domain-specific features (e.g. distances, ratios, indices).
    (Paste the exact logic from your training notebook/script here)
    """
    # Replace this placeholder with the exact body of your engineer_domain_features function
    df = df.copy()
    return df