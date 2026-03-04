from fastapi import APIRouter
from app.features.grievance.services.preprocessing import load_data
from app.features.grievance.services.clustering import cluster_complaints
from app.features.grievance.services.anomaly import detect_spike
from app.features.grievance.services.time_anomaly import detect_recent_spike

router = APIRouter(prefix="/grievance", tags=["Grievance"])


@router.get("/recent-spikes")
def recent_spikes():
    df = load_data()
    spikes = detect_recent_spike(df)

    return {
        "recent_spikes": spikes
    }


@router.get("/cluster")
def cluster_grievances():
    df = load_data()

    labels, keywords = cluster_complaints(df["cleaned"])

    return {
        "total_records": len(labels),
        "unique_clusters": len(set(labels)),
        "cluster_keywords": keywords
    }


@router.get("/anomaly")
def anomaly_detection():
    df = load_data()

    alerts = detect_spike(df)

    return {
        "alert_count": len(alerts),
        "alerts": alerts[:10]
    }


@router.get("/heatmap")
def heatmap_data():
    df = load_data()

    state_counts = df.groupby("state").size()

    return state_counts.to_dict()


@router.get("/intelligence-dashboard")
def intelligence_dashboard():
    df = load_data()

    labels, keywords = cluster_complaints(df["cleaned"])
    df["cluster"] = labels

    state_counts = df.groupby("state").size().to_dict()

    spikes = detect_recent_spike(df)

    cluster_summary = (
        df.groupby(["cluster"])
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .to_dict(orient="records")
    )

    return {
        "total_records": len(df),
        "state_heatmap": state_counts,
        "cluster_summary": cluster_summary,
        "cluster_keywords": keywords,
        "recent_spikes": spikes
    }
