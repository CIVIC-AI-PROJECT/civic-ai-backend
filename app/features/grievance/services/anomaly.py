def detect_spike(df, threshold=20):
    grouped = df.groupby(["state", "issue"]).size().reset_index(name="count")

    alerts = grouped[grouped["count"] > threshold]

    return alerts.to_dict(orient="records")
