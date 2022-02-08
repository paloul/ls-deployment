import hmac
import base64
import hashlib

username = b"paloul@me.com"
appClientId = b"68u17si0t3apv22e4o06h1i41t"
appClientSecret = b"clientsecretfromcognitouserpool"

signed = hmac.new(appClientSecret, username+appClientId, digestmod=hashlib.sha256)
secret_hash = base64.b64encode(signed.digest())
secret_hash