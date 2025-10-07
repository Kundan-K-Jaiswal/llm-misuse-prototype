# LLM Misuse Detection Prototype

This prototype demonstrates a minimal, modular architecture that addresses detection,
attribution, graph analysis, and dashboarding for AI-generated disinformation detection.

## Quick start (local, minimal)
1. Create a Python 3.10+ virtualenv and activate it.
2. `pip install -r requirements.txt`
3. Start backend: `uvicorn backend.app:app --reload --port 8000`
4. In another terminal run the simulator: `python scripts/ingest_simulator.py`
5. Open dashboard: `streamlit run dashboard/streamlit_app.py`

## Notes
- The HF transformer model is optional in backend/detection.py; the prototype uses stylometry heuristics by default.
- Change SECRET_KEY in backend/forensics.py before any real deployment.
