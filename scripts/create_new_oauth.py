#!/usr/bin/env python3
"""
새로운 OAuth 클라이언트 생성 가이드
기존 설정에 문제가 있을 때 사용
"""

import json
import os

def create_new_oauth_guide():
    """새로운 OAuth 클라이언트 생성 가이드"""
    print("🔧 새로운 OAuth 클라이언트 생성 가이드")
    print("=" * 50)
    
    print("\n기존 OAuth 설정에 문제가 있을 수 있습니다.")
    print("새로운 OAuth 클라이언트를 생성해보겠습니다.")
    
    print("\n📋 단계별 가이드:")
    print("1. Google Cloud Console 접속")
    print("   → https://console.cloud.google.com/")
    
    print("\n2. 새 프로젝트 생성 (선택사항)")
    print("   → 프로젝트 선택 → 새 프로젝트")
    print("   → 프로젝트 이름: AI-News-Blog-v2")
    
    print("\n3. Gmail API 활성화")
    print("   → API 및 서비스 → 라이브러리")
    print("   → Gmail API 검색 → 사용 설정")
    
    print("\n4. OAuth 동의 화면 설정")
    print("   → API 및 서비스 → OAuth 동의 화면")
    print("   → 외부 선택 → 만들기")
    print("   → 앱 정보:")
    print("     * 앱 이름: AI News Blog")
    print("     * 사용자 지원 이메일: winterkim.works@gmail.com")
    print("     * 개발자 연락처: winterkim.works@gmail.com")
    print("   → 저장 후 계속")
    
    print("\n5. 범위 추가")
    print("   → 범위 추가 또는 삭제")
    print("   → Gmail API 선택")
    print("   → https://www.googleapis.com/auth/gmail.send 추가")
    print("   → 저장 후 계속")
    
    print("\n6. 테스트 사용자 추가")
    print("   → 테스트 사용자")
    print("   → ADD USERS")
    print("   → winterkim.works@gmail.com 입력")
    print("   → 저장")
    
    print("\n7. OAuth 클라이언트 ID 생성")
    print("   → API 및 서비스 → 사용자 인증 정보")
    print("   → 사용자 인증 정보 만들기 → OAuth 클라이언트 ID")
    print("   → 애플리케이션 유형: 데스크톱 애플리케이션")
    print("   → 이름: AI News Blog Desktop")
    print("   → 만들기")
    
    print("\n8. 클라이언트 정보 복사")
    print("   → 클라이언트 ID와 클라이언트 보안 비밀번호 복사")

def setup_new_credentials():
    """새로운 인증 정보 설정"""
    print("\n" + "=" * 50)
    print("새로운 OAuth 클라이언트 정보를 입력하세요:")
    
    client_id = input("새 Client ID: ").strip()
    client_secret = input("새 Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID와 Client Secret을 모두 입력해야 합니다.")
        return False
    
    # 기존 파일 백업
    if os.path.exists('credentials.json'):
        os.rename('credentials.json', 'credentials_backup.json')
        print("✅ 기존 credentials.json을 credentials_backup.json으로 백업했습니다.")
    
    if os.path.exists('oauth_config.json'):
        os.rename('oauth_config.json', 'oauth_config_backup.json')
        print("✅ 기존 oauth_config.json을 oauth_config_backup.json으로 백업했습니다.")
    
    if os.path.exists('token.json'):
        os.remove('token.json')
        print("✅ 기존 token.json을 삭제했습니다.")
    
    # 새로운 설정 파일 생성
    credentials_info = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [
                "http://localhost:8080",
                "http://localhost:8081", 
                "http://localhost:8082"
            ]
        }
    }
    
    oauth_config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "sender_email": "winterkim.works@gmail.com",
        "recipients": [
            "winterkim.works@gmail.com",
            "iysin0102@gmail.com"
        ]
    }
    
    # 파일 저장
    with open('credentials.json', 'w') as f:
        json.dump(credentials_info, f, indent=2)
    
    with open('oauth_config.json', 'w') as f:
        json.dump(oauth_config, f, indent=2)
    
    print("✅ 새로운 OAuth 설정 파일이 생성되었습니다!")
    return True

def test_new_oauth():
    """새로운 OAuth 설정 테스트"""
    print("\n새로운 OAuth 설정을 테스트하시겠습니까? (y/n): ", end="")
    choice = input().lower()
    
    if choice == 'y':
        print("다음 명령어를 실행하세요:")
        print("python3 scripts/simple_oauth_test.py")

if __name__ == "__main__":
    create_new_oauth_guide()
    
    print("\n" + "=" * 50)
    choice = input("새로운 OAuth 클라이언트를 생성하셨나요? (y/n): ").lower()
    
    if choice == 'y':
        if setup_new_credentials():
            test_new_oauth()
    else:
        print("위 가이드를 따라 새로운 OAuth 클라이언트를 생성한 후 다시 실행하세요.") 