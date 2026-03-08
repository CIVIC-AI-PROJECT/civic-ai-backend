# Grievance Feature

## Purpose
Handles grievance intelligence APIs such as clustering, anomaly detection, spikes, and dashboard summaries.

## Endpoints
- `GET /grievance/recent-spikes`
- `GET /grievance/cluster`
- `GET /grievance/anomaly`
- `GET /grievance/heatmap`
- `GET /grievance/intelligence-dashboard`
- `POST /grievance/extract-entities`
- `POST /grievance/predictive-heatmap`

## Key Files
- `routes.py` → API endpoints for grievance analytics
- `services/preprocessing.py` → data loading and text cleaning
- `services/clustering.py` → clustering logic
- `services/anomaly.py` → anomaly/spike filtering
- `services/time_anomaly.py` → recent growth-based spike detection
- `services/entity_extraction.py` → location/official/issue entity extraction from complaint text
- `services/predictive.py` → predictive hotspot and anomaly alert generation
