#!/usr/bin/env python3
"""
OAuth 디버깅 스크립트 - 더 자세한 오류 정보 제공
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API 스코프
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def debug_oauth_flow():
    """OAuth 인증 과정을 단계별로 디버깅"""
    print("🔍 OAuth 디버깅 시작")
    print("=" * 40)
    
    # 1. 설정 파일 확인
    print("\n1. 설정 파일 확인:")
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json 파일이 없습니다!")
        return False
    
    with open('credentials.json', 'r') as f:
        creds_data = json.load(f)
    
    print("✅ credentials.json 존재")
    print(f"   Client ID: {creds_data['installed']['client_id'][:20]}...")
    print(f"   Redirect URIs: {creds_data['installed']['redirect_uris']}")
    
    # 2. 기존 토큰 확인
    print("\n2. 기존 토큰 확인:")
    creds = None
    if os.path.exists('token.json'):
        print("✅ 기존 토큰 발견")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("⚠️  기존 토큰 없음")
    
    # 3. 토큰 유효성 확인
    if creds and creds.valid:
        print("✅ 토큰이 유효합니다")
        return test_gmail_service(creds)
    
    # 4. 토큰 갱신 시도
    if creds and creds.expired and creds.refresh_token:
        print("🔄 토큰 갱신 시도...")
        try:
            creds.refresh(Request())
            print("✅ 토큰 갱신 성공")
            return test_gmail_service(creds)
        except Exception as e:
            print(f"❌ 토큰 갱신 실패: {e}")
    
    # 5. 새로운 인증 시도
    print("\n5. 새로운 OAuth 인증 시도:")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # 포트를 명시적으로 지정
        print("🌐 브라우저에서 인증을 진행합니다...")
        print("📝 인증 URL이 자동으로 열리지 않으면 수동으로 복사해서 브라우저에 붙여넣으세요.")
        
        creds = flow.run_local_server(port=8080, open_browser=True)
        
        # 토큰 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        print("✅ 인증 성공! 토큰이 저장되었습니다.")
        return test_gmail_service(creds)
        
    except Exception as e:
        print(f"❌ OAuth 인증 실패: {e}")
        print("\n🔧 가능한 해결책:")
        print("1. Google Cloud Console에서 테스트 사용자 추가")
        print("2. OAuth 동의 화면 설정 완료")
        print("3. Gmail API 활성화 확인")
        return False

def test_gmail_service(creds):
    """Gmail 서비스 테스트"""
    try:
        print("\n6. Gmail 서비스 테스트:")
        service = build('gmail', 'v1', credentials=creds)
        
        # 프로필 정보 가져오기 (권한 테스트)
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Gmail 연결 성공!")
        print(f"   이메일: {profile.get('emailAddress')}")
        print(f"   총 메시지 수: {profile.get('messagesTotal', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gmail 서비스 테스트 실패: {e}")
        return False

def print_troubleshooting():
    """문제 해결 가이드"""
    print("\n" + "=" * 50)
    print("🚨 문제 해결 가이드")
    print("=" * 50)
    
    print("\n가장 흔한 '액세스 차단됨' 오류 원인:")
    print("1. ❌ 테스트 사용자 미추가")
    print("   → OAuth 동의 화면에서 winterkim.works@gmail.com 추가")
    
    print("\n2. ❌ OAuth 동의 화면 미완성")
    print("   → 앱 이름, 지원 이메일, 개발자 연락처 입력")
    
    print("\n3. ❌ Gmail API 비활성화")
    print("   → API 라이브러리에서 Gmail API 활성화")
    
    print("\n4. ❌ 잘못된 리디렉션 URI")
    print("   → http://localhost:8080 정확히 입력")
    
    print("\n📋 체크리스트:")
    print("□ OAuth 동의 화면 → 테스트 사용자에 winterkim.works@gmail.com 추가")
    print("□ OAuth 동의 화면 → 앱 정보 모두 입력")
    print("□ API 라이브러리 → Gmail API 활성화")
    print("□ 사용자 인증 정보 → 리디렉션 URI에 http://localhost:8080 추가")

if __name__ == "__main__":
    success = debug_oauth_flow()
    if not success:
        print_troubleshooting()
    else:
        print("\n🎉 OAuth 설정이 완료되었습니다!")
        print("이제 다음 명령어로 이메일을 보낼 수 있습니다:")
        print("python3 scripts/main_automation_oauth.py test-email") 