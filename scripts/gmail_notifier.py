#!/usr/bin/env python3
"""
Gmail API를 사용하여 마일스톤 진행 상황을 이메일로 알리는 스크립트
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import json

class GmailNotifier:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
    
    def send_milestone_notification(self, milestone_name, status, details="", recipients=None):
        """마일스톤 알림 이메일 발송"""
        if recipients is None:
            recipients = [self.sender_email, "iysin0102@gmail.com"]
        
        # 이메일 제목
        subject = f"🚀 AI News Blog - {milestone_name} {status}"
        
        # 이메일 본문
        body = self.create_email_body(milestone_name, status, details)
        
        # 이메일 발송
        return self.send_email(recipients, subject, body)
    
    def create_email_body(self, milestone_name, status, details):
        """이메일 본문 생성"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        status_emoji = {
            "시작": "🚀",
            "진행중": "⚡",
            "완료": "✅",
            "실패": "❌",
            "대기": "⏳"
        }
        
        emoji = status_emoji.get(status, "📝")
        
        body = f"""
{emoji} AI News Blog 자동화 시스템 알림

📋 마일스톤: {milestone_name}
📊 상태: {status}
🕐 시간: {timestamp}

{details}

---
🔗 GitHub 저장소: https://github.com/winterkim-bot/sans
🌐 블로그 주소: https://winterkim-bot.github.io/sans

이 메시지는 자동으로 발송되었습니다.
        """
        
        return body.strip()
    
    def send_email(self, recipients, subject, body):
        """실제 이메일 발송"""
        try:
            # 이메일 메시지 생성
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipients)
            message["Subject"] = subject
            
            # 본문 추가
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            # SMTP 서버 연결 및 이메일 발송
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                text = message.as_string()
                server.sendmail(self.sender_email, recipients, text)
            
            print(f"✅ 이메일 발송 성공: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            print(f"❌ 이메일 발송 실패: {e}")
            return False
    
    def send_blog_update_notification(self, post_count, post_titles=None):
        """블로그 업데이트 알림"""
        if post_titles is None:
            post_titles = []
        
        subject = f"📰 AI News Blog 업데이트 - {post_count}개 새 포스트"
        
        body = f"""
📰 AI News Blog가 업데이트되었습니다!

📊 새로 추가된 포스트: {post_count}개
🕐 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 새 포스트 목록:
"""
        
        for i, title in enumerate(post_titles[:10], 1):  # 최대 10개만 표시
            body += f"{i}. {title}\n"
        
        if len(post_titles) > 10:
            body += f"... 외 {len(post_titles) - 10}개\n"
        
        body += f"""
🌐 블로그 확인하기: https://winterkim-bot.github.io/sans

---
이 메시지는 자동으로 발송되었습니다.
        """
        
        recipients = [self.sender_email, "iysin0102@gmail.com"]
        return self.send_email(recipients, subject, body.strip())

def load_email_config():
    """이메일 설정 로드"""
    config_file = "email_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # 설정 파일이 없으면 환경변수에서 읽기
        return {
            "sender_email": os.getenv("GMAIL_EMAIL"),
            "sender_password": os.getenv("GMAIL_APP_PASSWORD")
        }

def create_email_config_template():
    """이메일 설정 템플릿 생성"""
    config = {
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "note": "Gmail 앱 비밀번호를 사용하세요. 일반 비밀번호가 아닙니다!"
    }
    
    with open("email_config.json.template", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📧 email_config.json.template 파일이 생성되었습니다.")
    print("이 파일을 email_config.json으로 복사하고 실제 정보를 입력하세요.")

if __name__ == "__main__":
    # 설정 파일 템플릿 생성
    create_email_config_template()
    
    # 테스트 이메일 발송
    config = load_email_config()
    
    if config.get("sender_email") and config.get("sender_password"):
        notifier = GmailNotifier(config["sender_email"], config["sender_password"])
        
        # 테스트 알림 발송
        notifier.send_milestone_notification(
            "시스템 테스트", 
            "완료", 
            "Gmail 연동 시스템이 정상적으로 작동합니다! 🎉"
        )
    else:
        print("❌ 이메일 설정이 필요합니다. email_config.json 파일을 설정하세요.") 