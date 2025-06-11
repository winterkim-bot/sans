#!/usr/bin/env python3
"""
간단한 OAuth 테스트 - 문제 격리용
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API 스코프
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def simple_oauth_test():
    """가장 간단한 OAuth 테스트"""
    print("🔧 간단한 OAuth 테스트")
    print("=" * 30)
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json 파일이 없습니다!")
        return
    
    try:
        # OAuth 플로우 생성
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        print("🌐 OAuth 인증을 시작합니다...")
        print("브라우저가 열리면 Google 계정으로 로그인하세요.")
        print("만약 '액세스 차단됨' 오류가 나오면:")
        print("1. Google Cloud Console → OAuth 동의 화면")
        print("2. 테스트 사용자에 winterkim.works@gmail.com 추가")
        print("3. 앱 정보 모두 입력 (이름, 지원 이메일, 개발자 연락처)")
        
        # 다른 포트로 시도
        ports_to_try = [8080, 8081, 8082, 9090]
        
        for port in ports_to_try:
            try:
                print(f"\n포트 {port}으로 시도 중...")
                creds = flow.run_local_server(
                    port=port, 
                    open_browser=True,
                    success_message='인증이 완료되었습니다! 이 창을 닫아도 됩니다.'
                )
                
                # 토큰 저장
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                
                print(f"✅ 포트 {port}에서 인증 성공!")
                print("토큰이 저장되었습니다.")
                return True
                
            except Exception as e:
                print(f"포트 {port} 실패: {e}")
                continue
        
        print("❌ 모든 포트에서 실패했습니다.")
        return False
        
    except Exception as e:
        print(f"❌ OAuth 설정 오류: {e}")
        
        if "access_blocked" in str(e).lower():
            print("\n🚨 '액세스 차단됨' 오류 해결 방법:")
            print("1. https://console.cloud.google.com/apis/credentials/consent")
            print("2. 테스트 사용자 섹션에서 'ADD USERS' 클릭")
            print("3. winterkim.works@gmail.com 추가")
            print("4. 저장 후 다시 시도")
        
        return False

def check_google_cloud_settings():
    """Google Cloud Console 설정 체크리스트"""
    print("\n📋 Google Cloud Console 설정 체크리스트")
    print("=" * 45)
    
    print("\n✅ 확인해야 할 항목들:")
    print("□ 1. Gmail API 활성화")
    print("    → https://console.cloud.google.com/apis/library/gmail.googleapis.com")
    
    print("\n□ 2. OAuth 동의 화면 설정")
    print("    → https://console.cloud.google.com/apis/credentials/consent")
    print("    - 앱 이름: AI News Blog")
    print("    - 사용자 지원 이메일: winterkim.works@gmail.com")
    print("    - 개발자 연락처: winterkim.works@gmail.com")
    
    print("\n□ 3. 테스트 사용자 추가 (가장 중요!)")
    print("    - 테스트 사용자 섹션에서 'ADD USERS' 클릭")
    print("    - winterkim.works@gmail.com 입력")
    
    print("\n□ 4. OAuth 클라이언트 ID 설정")
    print("    → https://console.cloud.google.com/apis/credentials")
    print("    - 승인된 리디렉션 URI:")
    print("      * http://localhost:8080")
    print("      * http://localhost:8081")
    print("      * http://localhost:8082")

if __name__ == "__main__":
    check_google_cloud_settings()
    
    input("\n위 설정들을 모두 확인했으면 Enter를 눌러 OAuth 테스트를 시작하세요...")
    
    success = simple_oauth_test()
    
    if success:
        print("\n🎉 OAuth 인증 성공!")
        print("이제 이메일을 보낼 수 있습니다.")
    else:
        print("\n❌ OAuth 인증 실패")
        print("Google Cloud Console 설정을 다시 확인해주세요.") 