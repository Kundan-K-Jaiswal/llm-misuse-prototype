# forensics.py
import hashlib
import hmac
import base64

SECRET_KEY = b'your_prototype_secret_key_change_me'

class Forensics:
    def __init__(self, secret: bytes = None):
        self.secret = secret or SECRET_KEY

    def fingerprint(self, text: str) -> str:
        # SHA256 fingerprint
        h = hashlib.sha256()
        h.update(text.encode('utf-8'))
        return h.hexdigest()

    def embed_watermark(self, text: str, obj_id: str) -> dict:
        # Prototype reversible watermark using HMAC + short token
        mac = hmac.new(self.secret, msg=(obj_id + text).encode('utf-8'), digestmod=hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(mac)[:16].decode('ascii')
        return {'watermark_token': token}

    def verify_watermark(self, text: str, obj_id: str, token: str) -> bool:
        expected = self.embed_watermark(text, obj_id)['watermark_token']
        return hmac.compare_digest(expected, token)
