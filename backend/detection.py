# # detection.py
# import math
# try:
#     from transformers import pipeline
# except Exception:
#     pipeline = None
# from backend.stylometry import extract_stylometry_features

# class Detector:
#     def __init__(self, hf_model: str = None):
#         # If a model name is provided, load HF text-classification pipeline
#         self.hf_model = hf_model
#         self.hf = None
#         if hf_model and pipeline:
#             try:
#                 self.hf = pipeline('text-classification', model=hf_model)
#             except Exception as e:
#                 print('Warning: HF model load failed, fallback to stylometry only:', e)
#                 self.hf = None

#     def analyze(self, text: str):
#         # 1) Stylometric features
#         features = extract_stylometry_features(text)

#         # 2) HF detector score if available
#         hf_score = None
#         if self.hf:
#             try:
#                 out = self.hf(text[:1000])  # cap length
#                 hf_score = out
#             except Exception as e:
#                 hf_score = None

#         # 3) Heuristic combined score (prototype):
#         p_ai = self._heuristic_score(features)

#         combined = {
#             'heuristic_ai_prob': p_ai,
#             'stylometry': features,
#             'hf_raw': hf_score
#         }
#         return combined

#     def _heuristic_score(self, features: dict):
#         # Simple mapping from features to a [0,1] likelihood
#         score = 0.0
#         score += min(1.0, features.get('avg_word_length',0) / 6.0)
#         score += min(1.0, features.get('avg_sentence_length',0) / 25.0)
#         score += min(1.0, features.get('punctuation_ratio',0) * 5.0)
#         score += max(0, 1.0 - features.get('char_entropy',0) / 4.5)
#         score = score / 4.0
#         return round(float(score), 4)





import math
import re
from collections import Counter

# Optional: if you have a transformer model for AI detection, import it
# from transformers import AutoTokenizer, AutoModelForSequenceClassification

STOPWORDS = set([
    "the","be","to","of","and","a","in","that","have","I","it","for",
    "not","on","with","he","as","you","do","at","this","but","his",
    "by","from","they","we","say","her","she","or","an","will","my",
    "one","all","would","there","their","what","so","up","out","if",
    "about","who","get","which","go","me"
])

# ------------------ Helper functions ------------------

def tokenize_words(text):
    return [w for w in re.split(r'\W+', text.lower()) if w]

def split_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def char_entropy(text):
    if not text: return 0
    freq = Counter(text)
    n = len(text)
    return -sum((count/n) * math.log2(count/n) for count in freq.values())

def repetition_score(sentences):
    if not sentences: return 0
    counts = Counter(s.lower() for s in sentences)
    dup = sum(v-1 for v in counts.values() if v>1)
    return dup / len(sentences)

def punctuation_density(text):
    if not text: return 0
    puncts = re.findall(r'[.,;:!?"()\-]', text)
    return len(puncts) / len(text)

def stopword_ratio(words):
    if not words: return 0
    return sum(1 for w in words if w in STOPWORDS)/len(words)

def normalize(value, min_val, max_val):
    if max_val==min_val: return 0.5
    return min(1, max(0, (value - min_val)/(max_val - min_val)))

# ------------------ Main detection function ------------------

def detect_ai(text, model_score=None):
    """
    Returns a dictionary with:
      - score: 0-100 probability AI
      - verdict: Likely Human / Unsure / Likely AI
      - metrics: breakdown of signals
    Optionally combines with a transformer-based model score (0..1 float).
    """
    words = tokenize_words(text)
    sentences = split_sentences(text)
    word_count = len(words)
    sentence_count = len(sentences) or 1
    avg_words_per_sentence = word_count / sentence_count
    avg_word_length = sum(len(w) for w in words)/word_count if word_count>0 else 0
    p_density = punctuation_density(text)
    sw_ratio = stopword_ratio(words)
    rep_score = repetition_score(sentences)
    entropy = char_entropy(text)

    # Heuristic normalization ranges (tunable)
    entropy_norm = 1 - normalize(entropy, 3.0, 4.8)        # low entropy => AI-like
    avg_word_len_norm = normalize(avg_word_length, 3.4, 5.2) # longer words => human-like
    avg_words_per_sentence_norm = 1 - normalize(avg_words_per_sentence, 8, 18) # short sentences => AI
    punctuation_norm = 1 - normalize(p_density, 0.002, 0.02)  # low punctuation => AI
    stopword_norm = 1 - normalize(sw_ratio, 0.25, 0.45)     # lower stopwords => AI-ish
    rep_norm = normalize(rep_score, 0, 0.25)                 # repetition => AI-ish

    # Weights for signals
    weights = {
        'entropy': 0.28,
        'avg_word_len': 0.12,
        'avg_words_per_sentence': 0.18,
        'punctuation': 0.12,
        'stopword': 0.10,
        'repetition': 0.20
    }

    combined = (entropy_norm*weights['entropy'] +
                avg_word_len_norm*weights['avg_word_len'] +
                avg_words_per_sentence_norm*weights['avg_words_per_sentence'] +
                punctuation_norm*weights['punctuation'] +
                stopword_norm*weights['stopword'] +
                rep_norm*weights['repetition'])

    # Optionally combine with transformer model score
    if model_score is not None:
        # simple weighted average: 70% heuristic, 30% model
        combined = 0.7*combined + 0.3*model_score

    final_score = round(combined*100)

    # Verdict
    if final_score < 30:
        verdict = 'Likely Human'
    elif final_score < 60:
        verdict = 'Unsure'
    else:
        verdict = 'Likely AI'

    metrics = {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_words_per_sentence': avg_words_per_sentence,
        'avg_word_length': avg_word_length,
        'punctuation_density': p_density,
        'stopword_ratio': sw_ratio,
        'repetition_score': rep_score,
        'char_entropy': entropy
    }

    return {
        'score': final_score,
        'verdict': verdict,
        'metrics': metrics
    }

# ------------------ Example usage ------------------

if __name__ == '__main__':
    sample_text = "This is an example sentence written to demonstrate the AI detection feature."
    result = detect_ai(sample_text)
    print(result)

