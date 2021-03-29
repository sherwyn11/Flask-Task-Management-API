import jwt

from app.models.user import User

def auth_middleware(token):
    try:
        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')
        user = User.query.filter_by(id=payload['sub']).first()
        if user and token == user.token:
            return user
        else:
            return None
    except:
        return None