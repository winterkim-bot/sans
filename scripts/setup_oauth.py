#!/usr/bin/env python3
"""
Gmail OAuth 설정 도우미 스크립트
"""

import json
import os

def create_oauth_setup():
    """OAuth 설정 가이드"""
    print("🔧 Gmail OAuth 설정 가이드")
    print("=" * 50)
    
    print("\n1. Google Cloud Console 설정:")
    print("   - https://console.cloud.google.com/ 접속")
    print("   - 프로젝트 선택 또는 새 프로젝트 생성")
    print("   - API 및 서비스 → 라이브러리 → Gmail API 활성화")
    
    print("\n2. OAuth 동의 화면 설정:")
    print("   - API 및 서비스 → OAuth 동의 화면")
    print("   - 외부 사용자 유형 선택")
    print("   - 앱 이름: 'AI News Blog'")
    print("   - 사용자 지원 이메일: winterkim.works@gmail.com")
    print("   - 개발자 연락처 정보: winterkim.works@gmail.com")
    
    print("\n3. OAuth 클라이언트 ID 생성:")
    print("   - API 및 서비스 → 사용자 인증 정보")
    print("   - 사용자 인증 정보 만들기 → OAuth 클라이언트 ID")
    print("   - 애플리케이션 유형: 데스크톱 애플리케이션")
    print("   - 이름: 'AI News Blog Desktop'")
    
    print("\n4. 승인된 리디렉션 URI 추가:")
    print("   - http://localhost:8080")
    print("   - http://localhost")
    
    print("\n5. 테스트 사용자 추가:")
    print("   - OAuth 동의 화면 → 테스트 사용자")
    print("   - winterkim.works@gmail.com 추가")
    print("   - iysin0102@gmail.com 추가")
    
    print("\n6. 클라이언트 정보 입력:")
    client_id = input("Client ID를 입력하세요: ").strip()
    client_secret = input("Client Secret을 입력하세요: ").strip()
    
    if client_id and client_secret:
        update_oauth_config(client_id, client_secret)
    else:
        print("❌ Client ID와 Client Secret을 모두 입력해야 합니다.")

def update_oauth_config(client_id, client_secret):
    """OAuth 설정 파일 업데이트"""
    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "sender_email": "winterkim.works@gmail.com",
        "recipients": [
            "winterkim.works@gmail.com",
            "iysin0102@gmail.com"
        ]
    }
    
    # oauth_config.json 업데이트
    with open("oauth_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    # credentials.json 업데이트
    credentials_info = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost:8080", "http://localhost"]
        }
    }
    
    with open('credentials.json', 'w') as f:
        json.dump(credentials_info, f, indent=2)
    
    print("✅ OAuth 설정 파일이 업데이트되었습니다!")
    print("\n다음 명령어로 테스트하세요:")
    print("python3 scripts/main_automation_oauth.py test-email")

def check_current_config():
    """현재 설정 확인"""
    print("📋 현재 OAuth 설정:")
    
    if os.path.exists("oauth_config.json"):
        with open("oauth_config.json", 'r') as f:
            config = json.load(f)
        
        print(f"Client ID: {config.get('client_id', 'Not set')}")
        print(f"Client Secret: {'Set' if config.get('client_secret') and config.get('client_secret') != 'your-client-secret-here' else 'Not set'}")
        print(f"Sender Email: {config.get('sender_email', 'Not set')}")
        
        if config.get('client_secret') == 'your-client-secret-here':
            print("⚠️  Client Secret이 설정되지 않았습니다!")
            return False
        return True
    else:
        print("❌ oauth_config.json 파일이 없습니다.")
        return False

if __name__ == "__main__":
    print("🔧 Gmail OAuth 설정 도우미")
    print("=" * 30)
    
    if check_current_config():
        choice = input("\n설정을 다시 하시겠습니까? (y/n): ").lower()
        if choice == 'y':
            create_oauth_setup()
    else:
        create_oauth_setup() 