# utils.py
from flask_bcrypt import Bcrypt
#Bcrypt는 해시 함수를 사용하여 비밀번호를 안전하게 저장하고 검증하는 데 사용

#bcrypt 객체 초기화
bcrypt = Bcrypt()
#유효하지 않은 토큰을 저장하는 데 사용되는 빈 집합(set)을 정의
invalid_tokens = set()

#비밀번호를 해시화하는 함수를 정의
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
#주어진 비밀번호를 해시화하여 반환
#generate_password_hash Bcrypt 알고리즘을 사용하여 안전한 해시를 생성 후 
#decode('utf-8') : 바이트 문자열을 유니코드 문자열로 변환하여 반환

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
