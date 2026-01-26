from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token is valid but expired
        return None
    except JWTError:
        # Token is invalid (wrong signature, malformed, etc.)
        return None
    except Exception:
        # Catch absolutely everything else
        return None