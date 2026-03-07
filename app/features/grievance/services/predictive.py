import pandas as pd


def build_predictive_heatmap(df: pd.DataFrame, alert_window_hours: int = 24, min_alert_count: int = 5):
    if df.empty:
        return {
            "heatmap": [],
            "alerts": [],
            "total_complaints": 0,
        }

    location_cols = ["state", "village", "issue"]
    grouped = (
        df.groupby(location_cols)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    heatmap = grouped.to_dict(orient="records")

    if "received_at" in df.columns:
        latest = df["received_at"].max()
        if pd.isna(latest):
            window_df = df
        else:
            window_start = latest - pd.Timedelta(hours=alert_window_hours)
            window_df = df[df["received_at"] >= window_start]
    else:
        window_df = df

    window_grouped = (
        window_df.groupby(location_cols)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    alerts = window_grouped[window_grouped["count"] >= min_alert_count].copy()
    if alerts.empty:
        alerts["message"] = pd.Series(dtype=str)
    else:
        alerts["message"] = alerts.apply(
            lambda row: (
                f"Anomaly Detected: {int(row['count'])} complaints regarding "
                f"'{row['issue']}' from village '{row['village']}' in last {alert_window_hours}h"
            ),
            axis=1,
        )

    return {
        "heatmap": heatmap,
        "alerts": alerts.to_dict(orient="records"),
        "total_complaints": int(len(df)),
    }
