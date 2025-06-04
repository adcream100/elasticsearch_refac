

from pydantic_settings import BaseSettings, SettingsConfigDict
from pytz import timezone
from pathlib import Path
from enum import Enum
from typing import List, Dict, Any, ClassVar, Optional


class Settings(BaseSettings):
    # Redis 설정
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6380
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = "" 

    # MSSQL 설정
    mssql_lib: str
    mssql_host: str
    mssql_port: str
    mssql_user: str
    mssql_pass: str
    mssql_db: str
    mssql_db_temp: str
    mssql_driver: str

    # Elasticsearch 설정
    elastic_node: str
    elastic_user: str
    elastic_password: str
    elastic_ca_cert_path: str

    # 기타 설정
    secret_key: str
    project_state: str
    app_name: str
    env: str
    app_url: str
    sso_url: str
    USER_IMG_URL: str
    sb_img_url: str
    cut_img_url: str
    profile_image_url: str
    access_token_cookie_name: str
    sso_allow_origin_dev: str
    sso_allow_origin: str
    allowed_domains: str
    tvcf_sso_cookie_name: str
    tvcf_mail_username: str
    tvcf_mail_password: str
    tvcf_mail_from: str
    tvcf_mail_port: str
    tvcf_mail_server: str
    tvcf_mail_starttls: str
    tvcf_mail_ssl_tls: str
    tvcf_use_credentials: str
    tvcf_validate_certs: str

    @property
    def TIMEZONE_KST(self) -> Any:
        return timezone('Asia/Seoul')
    
    # config.py에서 이동한 상수들
    JOB_PORTFOLIO_MAX_WIDTH: int = 1280
    GIF_DELAY: int = 2400
    GIF_WIDTH: int = 350
    GIF_HEIGHT: int = 196
    THIS_FOLDER_TMP: str = "TMP"
    IS_DEVELOPMENT: bool = True
    DEV_DATE: str = "20240503"

    # 알림 서비스 관련 설정 추가
    SMTP_SENDER: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    ADMIN_EMAIL: str
    WEBHOOK_URL: str


    # model_config = SettingsConfigDict(env_file=".env", extra="allow")
    model_config = SettingsConfigDict(env_file=(".env", "utf-8"), extra="allow")

settings = Settings()

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class PaymentSettings(BaseSettings):
    # 환경 설정
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    # 토스페이먼츠 키 설정
    TOSS_CLIENT_KEY: str
    TOSS_SECRET_KEY: str
    TOSS_LIVE_CLIENT_KEY: Optional[str] = None
    TOSS_LIVE_SECRET_KEY: Optional[str] = None




    # CST_PLATFORM: str = "service"  # 실 서버는 "service", 테스트는 "test"
    CST_PLATFORM: str = "test"      # 테스트 환경
    IS_TEST_MODE: bool = True       # 테스트 모드 활성화
    
    '''
    # [테스트 카드 정보]
    # 카드번호: 4111-1111-1111-1111
    # 만료일: 12/24
    # CVC: 123
    '''

    # 도메인 및 결제 관련 URL 설정
    BASE_DOMAIN: str = "dev.tvcf.co.kr"
    FRONT_DOMAIN: str = "front.tvcf.co.kr"
    PAYMENT_URL: str = f"https://{FRONT_DOMAIN}/payment"

    SUPPORT_CONTACT: str = "02-3447-0101"
    SUPPORT_EMAIL: str = "support@tvcf.co.kr"
    
    # PG API 엔드포인트

    TOSS_API_URL: str = "https://api.tosspayments.com"
    TOSS_PAY_URL: str = f"{TOSS_API_URL}/v1"
    LGD_PAY_URL: str = "https://pgapi.tosspayments.com/v2/payments"
    LGD_CANCEL_URL: str = "https://pgapi.tosspayments.com/v1/payments/cancel"
    
    # 결제 취소 권한 설정
    PAYMENT_CANCEL_ALLOWED_ROLES: List[int] = [3, 4, 5, 6, 7]  # 관리자 권한을 가진 usertype
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    PAYMENT_LOG_DIR: Path = Path("logs/payment")
    PAYMENT_ERROR_LOG_FILE: str = "payment_error.log"
    PAYMENT_ACCESS_LOG_FILE: str = "payment_access.log"
    
    # 결제 상태 코드
    PAYMENT_STATUS_SUCCESS: str = "0000"  # PG사 성공 응답 코드
    
    
    # 테스트 모드 설정
    IS_TEST_MODE: bool = True

    # 테스트용 설정 (ClassVar로 정의)
    TEST_PG_CONFIG: ClassVar[Dict[str, str]] = {
        "CST_PLATFORM": "test",
        "CST_MID": "tvcf3447",
        "LGD_MID": "ttvcf3447",  # 테스트용 상점 ID에는 't' 접두어 필요
    }

    TEST_CARD_INFO: ClassVar[Dict[str, str]] = {
        "card_number": "9100000000000000",
        "expiry_date": "12/25",
        "birth": "800101",
        "card_pwd": "00"
    }

    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    @property
    def active_toss_client_key(self) -> str:
        """현재 환경에 맞는 클라이언트 키 반환"""
        if self.is_production and self.TOSS_LIVE_CLIENT_KEY:
            return self.TOSS_LIVE_CLIENT_KEY
        return self.TOSS_CLIENT_KEY
    
    @property
    def active_toss_secret_key(self) -> str:
        """현재 환경에 맞는 시크릿 키 반환"""
        if self.is_production and self.TOSS_LIVE_SECRET_KEY:
            return self.TOSS_LIVE_SECRET_KEY
        return self.TOSS_SECRET_KEY

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }




# 설정 인스턴스 생성
payment_settings = PaymentSettings()