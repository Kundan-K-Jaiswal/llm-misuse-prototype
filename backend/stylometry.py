# stylometry.py
import math
from collections import Counter

def avg_word_length(words):
    if not words:
        return 0
    return sum(len(w) for w in words) / len(words)

def avg_sentence_length(sentences):
    if not sentences:
        return 0
    return sum(len(s.split()) for s in sentences) / len(sentences)

def punctuation_ratio(text):
    if not text:
        return 0
    punct = sum(1 for c in text if c in '.!,;:?')
    return punct / max(1, len(text))

def char_entropy(text):
    if not text:
        return 0
    counts = Counter(text)
    total = len(text)
    probs = [v/total for v in counts.values()]
    ent = -sum(p * math.log(p+1e-12, 2) for p in probs)
    return ent

def extract_stylometry_features(text: str) -> dict:
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    words = [w for w in text.replace('\n', ' ').split() if w]
    features = {
        'avg_word_length': avg_word_length(words),
        'avg_sentence_length': avg_sentence_length(sentences),
        'punctuation_ratio': punctuation_ratio(text),
        'char_entropy': char_entropy(text),
        'word_count': len(words)
    }
    return features
