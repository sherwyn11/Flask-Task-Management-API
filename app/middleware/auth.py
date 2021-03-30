import jwt
from app.models.user import User
from config.deployment import JWT_SECRET

def auth_middleware(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms='HS256')
        user = User.query.filter_by(id=payload['sub']).first()
        if user and token == user.token:
            return user
        else:
            return None
    except:
        return None