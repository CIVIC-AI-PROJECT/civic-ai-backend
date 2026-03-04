import pandas as pd


def detect_recent_spike(df, days=7, growth_threshold=0.5):
    latest_date = df["date_received"].max()

    recent_start = latest_date - pd.Timedelta(days=days)
    previous_start = recent_start - pd.Timedelta(days=days)

    recent_df = df[df["date_received"] >= recent_start]
    previous_df = df[
        (df["date_received"] >= previous_start) &
        (df["date_received"] < recent_start)
    ]

    recent_counts = (
        recent_df.groupby(["state", "issue"])
        .size()
        .reset_index(name="recent_count")
    )

    previous_counts = (
        previous_df.groupby(["state", "issue"])
        .size()
        .reset_index(name="previous_count")
    )

    merged = pd.merge(
        recent_counts,
        previous_counts,
        on=["state", "issue"],
        how="left"
    )

    merged["previous_count"] = merged["previous_count"].fillna(0)

    merged["growth"] = (
        (merged["recent_count"] - merged["previous_count"]) /
        (merged["previous_count"] + 1)
    )

    spikes = merged[merged["growth"] > growth_threshold]

    return spikes.to_dict(orient="records")
