#!/usr/bin/env python3
"""
OAuth 설정 상태 확인 스크립트
"""

import json
import os

def check_oauth_files():
    """OAuth 관련 파일들 확인"""
    print("📋 OAuth 파일 상태 확인")
    print("=" * 30)
    
    # oauth_config.json 확인
    if os.path.exists("oauth_config.json"):
        print("✅ oauth_config.json 존재")
        with open("oauth_config.json", 'r') as f:
            config = json.load(f)
        
        print(f"   Client ID: {config.get('client_id', 'Not set')[:20]}...")
        print(f"   Client Secret: {'설정됨' if config.get('client_secret') and not config.get('client_secret').startswith('your-') else '설정 안됨'}")
        print(f"   Sender Email: {config.get('sender_email', 'Not set')}")
    else:
        print("❌ oauth_config.json 없음")
    
    # credentials.json 확인
    if os.path.exists("credentials.json"):
        print("✅ credentials.json 존재")
        with open("credentials.json", 'r') as f:
            creds = json.load(f)
        
        installed = creds.get('installed', {})
        print(f"   Redirect URIs: {installed.get('redirect_uris', [])}")
    else:
        print("❌ credentials.json 없음")
    
    # token.json 확인 (인증 완료 후 생성됨)
    if os.path.exists("token.json"):
        print("✅ token.json 존재 (인증 완료됨)")
    else:
        print("⚠️  token.json 없음 (인증 필요)")

def print_setup_guide():
    """설정 가이드 출력"""
    print("\n🔧 Google Cloud Console 설정 가이드")
    print("=" * 40)
    
    print("\n1. OAuth 동의 화면 설정:")
    print("   https://console.cloud.google.com/apis/credentials/consent")
    print("   - 외부 사용자 유형 선택")
    print("   - 앱 이름: AI News Blog")
    print("   - 사용자 지원 이메일: winterkim.works@gmail.com")
    print("   - 개발자 연락처: winterkim.works@gmail.com")
    print("   - 저장 후 '게시 상태로 푸시' 클릭")
    
    print("\n2. 테스트 사용자 추가:")
    print("   OAuth 동의 화면 → 테스트 사용자")
    print("   - winterkim.works@gmail.com")
    print("   - iysin0102@gmail.com")
    
    print("\n3. Gmail API 활성화:")
    print("   https://console.cloud.google.com/apis/library/gmail.googleapis.com")
    print("   - '사용' 버튼 클릭")
    
    print("\n4. OAuth 클라이언트 ID 설정:")
    print("   https://console.cloud.google.com/apis/credentials")
    print("   - 클라이언트 ID 클릭")
    print("   - 승인된 리디렉션 URI 추가:")
    print("     * http://localhost:8080")
    print("     * http://localhost")
    
    print("\n5. 중요: OAuth 동의 화면을 '게시됨' 상태로 변경")
    print("   - OAuth 동의 화면에서 '앱 게시' 버튼 클릭")
    print("   - 또는 테스트 사용자에 본인 이메일 추가")

if __name__ == "__main__":
    check_oauth_files()
    print_setup_guide()
    
    print("\n" + "=" * 50)
    print("설정 완료 후 다음 명령어로 테스트:")
    print("python3 scripts/main_automation_oauth.py test-email") 