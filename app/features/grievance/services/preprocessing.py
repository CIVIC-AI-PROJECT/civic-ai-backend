import os
import pandas as pd
import re

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "grievances.csv.zip")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\W+', ' ', text)
    return text


def load_data(limit=3000):
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "Consumer complaint narrative": "complaint_text",
        "State": "state",
        "Issue": "issue",
        "Date received": "date_received"
    })

    df = df.dropna(subset=["complaint_text"])

    df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce")

    df = df.head(limit)

    df["cleaned"] = df["complaint_text"].apply(clean_text)

    return df
