#!/usr/bin/env python3
"""
Gmail OAuth 인증 및 이메일 발송 시스템
Google Gmail API를 사용하여 OAuth 인증을 통해 이메일을 발송합니다.
"""

import os
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False
    print("⚠️  Gmail API 라이브러리가 설치되지 않았습니다.")
    print("다음 명령어로 설치하세요: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")

# Gmail API 스코프
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/userinfo.profile']

class GmailOAuthNotifier:
    def __init__(self):
        """Gmail OAuth 알림 시스템 초기화"""
        if not GMAIL_API_AVAILABLE:
            self.service = None
            return
            
        self.service = None
        self.sender_email = None
        self.recipients = []
        
        # OAuth 설정 로드
        self.load_config()
        
        # Gmail 서비스 초기화
        self.authenticate()
    
    def load_config(self):
        """OAuth 설정 파일 로드"""
        config_file = "oauth_config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.sender_email = config.get("sender_email", "")
                self.recipients = config.get("recipients", [])
        else:
            print("⚠️  oauth_config.json 파일이 없습니다.")
            print("scripts/gmail_oauth.py를 먼저 실행하여 OAuth 설정을 완료하세요.")
    
    def authenticate(self):
        """Gmail API OAuth 인증"""
        creds = None
        
        # 기존 토큰 파일이 있으면 로드
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # 유효한 자격 증명이 없으면 새로 인증
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"토큰 갱신 실패: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists('credentials.json'):
                    print("⚠️  credentials.json 파일이 없습니다.")
                    print("Google Cloud Console에서 OAuth 클라이언트 자격 증명을 다운로드하세요.")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # 토큰 저장
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API 인증 성공!")
        except Exception as e:
            print(f"❌ Gmail API 인증 실패: {e}")
            self.service = None
    
    def create_message(self, to, subject, body):
        """이메일 메시지 생성"""
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = self.sender_email
        message['subject'] = subject
        
        message.attach(MIMEText(body, 'html', 'utf-8'))
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
    
    def send_email(self, to, subject, body):
        """이메일 발송"""
        if not self.service:
            return False
        
        try:
            message = self.create_message(to, subject, body)
            result = self.service.users().messages().send(userId='me', body=message).execute()
            print(f"✅ 이메일 발송 성공: {to}")
            return True
        except HttpError as error:
            print(f"❌ 이메일 발송 실패 ({to}): {error}")
            return False
    
    def send_milestone_notification(self, milestone_info):
        """마일스톤 알림 이메일 발송"""
        if not self.service or not self.recipients:
            return False
        
        title = milestone_info.get('title', 'AI News Blog 알림')
        description = milestone_info.get('description', '')
        
        subject = f"🤖 AI News Blog - {title}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    🤖 AI News Blog 자동화 시스템
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #e74c3c; margin-top: 0;">📢 {title}</h3>
                    <p style="font-size: 16px; margin-bottom: 0;">{description}</p>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #27ae60;">
                        <strong>🕐 알림 시간:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        이 메시지는 AI News Blog 자동화 시스템에서 발송되었습니다.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        success_count = 0
        for recipient in self.recipients:
            if self.send_email(recipient, subject, body):
                success_count += 1
        
        return success_count > 0

def setup_oauth_config():
    """OAuth 설정 파일 생성"""
    print("🔧 Gmail OAuth 설정을 시작합니다...")
    
    # 기본 설정
    config = {
        "client_id": "",
        "client_secret": "",
        "sender_email": "winterkim.works@gmail.com",
        "recipients": [
            "winterkim.works@gmail.com",
            "iysin0102@gmail.com"
        ]
    }
    
    # OAuth 설정 파일 생성
    with open("oauth_config.json", "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ oauth_config.json 파일이 생성되었습니다.")
    print("📝 Google Cloud Console에서 client_id와 client_secret을 확인하여 oauth_config.json과 credentials.json 파일을 완성하세요.")
    
    # credentials.json 템플릿 생성
    credentials_template = {
        "installed": {
            "client_id": "",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open("credentials.json", "w") as f:
        json.dump(credentials_template, f, indent=2)
    
    print("✅ credentials.json 템플릿이 생성되었습니다.")
    print("⚠️  OAuth 인증을 완료한 후 다시 실행하세요.")

def main():
    """메인 함수"""
    if not GMAIL_API_AVAILABLE:
        return
    
    # OAuth 설정 확인
    if not os.path.exists("oauth_config.json") or not os.path.exists("credentials.json"):
        setup_oauth_config()
        return
    
    # Gmail OAuth 시스템 초기화
    notifier = GmailOAuthNotifier()
    
    if notifier.service:
        # 테스트 알림 발송
        test_notification = {
            "title": "시스템 테스트",
            "description": "Gmail OAuth 시스템이 정상적으로 작동합니다! 🎉"
        }
        notifier.send_milestone_notification(test_notification)
    else:
        print("❌ Gmail OAuth 인증에 실패했습니다.")

if __name__ == "__main__":
    main() 