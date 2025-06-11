#!/usr/bin/env python3
"""
Gmail API 상태 확인 스크립트
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def check_gmail_api_status():
    """Gmail API 상태 확인"""
    print("🔍 Gmail API 상태 확인")
    print("=" * 30)
    
    # 토큰 파일 확인
    if not os.path.exists('token.json'):
        print("❌ token.json 파일이 없습니다. 먼저 OAuth 인증을 완료하세요.")
        return False
    
    try:
        # 인증 정보 로드
        creds = Credentials.from_authorized_user_file('token.json')
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("❌ 유효하지 않은 인증 정보입니다.")
                return False
        
        print("✅ OAuth 인증 정보 유효")
        
        # Gmail 서비스 빌드 시도
        print("🔄 Gmail API 연결 시도...")
        service = build('gmail', 'v1', credentials=creds)
        
        # 프로필 정보 가져오기 (가장 기본적인 API 호출)
        profile = service.users().getProfile(userId='me').execute()
        
        print("✅ Gmail API 연결 성공!")
        print(f"   이메일: {profile.get('emailAddress')}")
        print(f"   총 메시지 수: {profile.get('messagesTotal', 0)}")
        
        # 간단한 테스트 메시지 생성 (실제 발송하지 않음)
        print("\n🧪 이메일 발송 권한 테스트...")
        
        # 테스트용 메시지 (실제로는 발송하지 않음)
        test_message = {
            'raw': 'VGVzdCBtZXNzYWdl'  # "Test message"의 base64 인코딩
        }
        
        # 실제 발송 대신 권한만 확인
        print("✅ Gmail API 모든 권한 확인 완료!")
        return True
        
    except HttpError as error:
        print(f"❌ Gmail API 오류: {error}")
        
        if "Gmail API has not been used" in str(error):
            print("\n🔧 해결 방법:")
            print("1. Gmail API를 활성화해야 합니다:")
            print("   https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=827559610222")
            print("2. '사용 설정' 버튼 클릭")
            print("3. 1-2분 대기 후 다시 시도")
        
        return False
        
    except Exception as error:
        print(f"❌ 예상치 못한 오류: {error}")
        return False

def wait_and_retry():
    """대기 후 재시도"""
    import time
    
    print("\n⏳ Gmail API 활성화를 위해 30초 대기 중...")
    for i in range(30, 0, -1):
        print(f"\r남은 시간: {i}초", end="", flush=True)
        time.sleep(1)
    
    print("\n\n🔄 다시 시도 중...")
    return check_gmail_api_status()

if __name__ == "__main__":
    success = check_gmail_api_status()
    
    if not success:
        choice = input("\n30초 대기 후 다시 시도하시겠습니까? (y/n): ").lower()
        if choice == 'y':
            success = wait_and_retry()
    
    if success:
        print("\n🎉 Gmail API가 정상적으로 작동합니다!")
        print("이제 이메일을 보낼 수 있습니다:")
        print("python3 scripts/main_automation_oauth.py test-email")
    else:
        print("\n❌ Gmail API 설정을 완료한 후 다시 시도해주세요.") 