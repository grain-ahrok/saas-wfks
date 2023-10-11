# utils.py
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
invalid_tokens = set()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

'''
---------------------------------------
수정 생각하고 있는 부분
from flask_bcrypt import Bcrypt
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

bcrypt = Bcrypt()
csrf = SeaSurf()
invalid_tokens = set()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def configure_security(app):
    # CSRF 보호 설정
    csrf.init_app(app)

    # Talisman을 사용한 보안 정책 설정
    talisman = Talisman(app)

    # Talisman 구성 옵션 설정 (예: HTTPS 강제, Content Security Policy 등)
    talisman.content_security_policy = {
        # 내용 보안 정책 설정
        "default-src": "'self'",
        "style-src": "'self' 'unsafe-inline'",
        "font-src": "'self' fonts.gstatic.com",
        "script-src": "'self'",
        "object-src": "'none'",
        "frame-ancestors": "'none'",
        "base-uri": "'self'",
        "form-action": "'self'",
        "frame-src": "'self'"
    }

    # 기타 Talisman 구성 옵션을 추가할 수 있습니다.


'''
