# detection.py
import math
try:
    from transformers import pipeline
except Exception:
    pipeline = None
from backend.stylometry import extract_stylometry_features

class Detector:
    def __init__(self, hf_model: str = None):
        # If a model name is provided, load HF text-classification pipeline
        self.hf_model = hf_model
        self.hf = None
        if hf_model and pipeline:
            try:
                self.hf = pipeline('text-classification', model=hf_model)
            except Exception as e:
                print('Warning: HF model load failed, fallback to stylometry only:', e)
                self.hf = None

    def analyze(self, text: str):
        # 1) Stylometric features
        features = extract_stylometry_features(text)

        # 2) HF detector score if available
        hf_score = None
        if self.hf:
            try:
                out = self.hf(text[:1000])  # cap length
                hf_score = out
            except Exception as e:
                hf_score = None

        # 3) Heuristic combined score (prototype):
        p_ai = self._heuristic_score(features)

        combined = {
            'heuristic_ai_prob': p_ai,
            'stylometry': features,
            'hf_raw': hf_score
        }
        return combined

    def _heuristic_score(self, features: dict):
        # Simple mapping from features to a [0,1] likelihood
        score = 0.0
        score += min(1.0, features.get('avg_word_length',0) / 6.0)
        score += min(1.0, features.get('avg_sentence_length',0) / 25.0)
        score += min(1.0, features.get('punctuation_ratio',0) * 5.0)
        score += max(0, 1.0 - features.get('char_entropy',0) / 4.5)
        score = score / 4.0
        return round(float(score), 4)
