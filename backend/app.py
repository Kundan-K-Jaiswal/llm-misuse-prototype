from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.detection import Detector
from backend.forensics import Forensics
from backend.graph_analysis import GraphEngine

app = FastAPI(title="LLM Misuse Detection Prototype")

# Instantiate modules (in production, use dependency injection)
detector = Detector()
forensics = Forensics()
graph = GraphEngine()

class ContentIn(BaseModel):
    id: str
    text: str
    source: str = "simulator"
    metadata: dict = {}

@app.post('/detect')
async def detect(payload: ContentIn):
    try:
        # Run detection
        result = detector.analyze(payload.text)
        # Create fingerprint
        fingerprint = forensics.fingerprint(payload.text)
        watermark = forensics.embed_watermark(payload.text, payload.id)
        # Add to graph engine
        graph.add_node(payload.id, payload.text, payload.metadata)
        return {
            'id': payload.id,
            'source': payload.source,
            'detection': result,
            'fingerprint': fingerprint,
            'watermark': watermark
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/graph/summary')
async def graph_summary():
    return graph.summary()

@app.get('/health')
async def health():
    return {'status': 'ok'}
