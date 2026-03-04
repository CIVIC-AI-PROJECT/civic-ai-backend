# Grievance Feature

## Purpose
Handles grievance intelligence APIs such as clustering, anomaly detection, spikes, and dashboard summaries.

## Endpoints
- `GET /grievance/recent-spikes`
- `GET /grievance/cluster`
- `GET /grievance/anomaly`
- `GET /grievance/heatmap`
- `GET /grievance/intelligence-dashboard`

## Key Files
- `routes.py` → API endpoints for grievance analytics
- `services/preprocessing.py` → data loading and text cleaning
- `services/clustering.py` → clustering logic
- `services/anomaly.py` → anomaly/spike filtering
- `services/time_anomaly.py` → recent growth-based spike detection
