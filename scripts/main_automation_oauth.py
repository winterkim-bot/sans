#!/usr/bin/env python3
"""
AI News Blog 자동화 스크립트 (OAuth 버전)
Excel 파일을 Markdown으로 변환하고 Git에 업로드한 후 Gmail OAuth를 통해 이메일 알림을 발송합니다.
"""

import os
import sys
import subprocess
import datetime
import glob
import json

# 현재 스크립트의 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from excel_to_markdown import excel_to_markdown
from gmail_oauth import GmailOAuthNotifier

class BlogAutomationOAuth:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.oauth_config = self.load_oauth_config()
        
        # OAuth 설정이 있으면 notifier 초기화
        if self.oauth_config.get("client_id"):
            self.notifier = GmailOAuthNotifier()  # 파라미터 없이 초기화
    
    def load_oauth_config(self):
        """OAuth 설정 로드"""
        config_file = os.path.join(self.project_root, "oauth_config.json")
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # 기본 설정 반환
            return {
                "client_id": "827559610222-ijmpggdvrgj736almhbda576l5l42l77.apps.googleusercontent.com",
                "sender_email": "winterkim.works@gmail.com",
                "recipients": ["winterkim.works@gmail.com", "iysin0102@gmail.com"]
            }
    
    def send_notification(self, milestone_info):
        """이메일 알림 발송"""
        if hasattr(self, 'notifier') and self.notifier and self.notifier.service:
            return self.notifier.send_milestone_notification(milestone_info)
        else:
            print(f"📧 알림: {milestone_info.get('title', 'N/A')} - {milestone_info.get('description', 'N/A')}")
            return True
    
    def run_git_command(self, command):
        """Git 명령어 실행"""
        try:
            os.chdir(self.project_root)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def process_excel_files(self):
        """Excel 파일들을 처리하여 Markdown으로 변환"""
        self.send_notification({
            "title": "데이터 처리 시작",
            "description": "Excel 파일을 Markdown으로 변환 중..."
        })
        
        # Excel 파일 찾기
        excel_files = glob.glob(os.path.join(self.project_root, "*.xlsx"))
        
        if not excel_files:
            self.send_notification({
                "title": "데이터 처리 실패",
                "description": "Excel 파일을 찾을 수 없습니다."
            })
            return False, []
        
        all_created_files = []
        
        for excel_file in excel_files:
            print(f"📊 Processing: {os.path.basename(excel_file)}")
            
            # 현재 디렉토리를 프로젝트 루트로 변경
            os.chdir(self.project_root)
            
            # Excel을 Markdown으로 변환
            created_files = excel_to_markdown(excel_file)
            all_created_files.extend(created_files)
        
        if all_created_files:
            self.send_notification({
                "title": "데이터 처리 완료",
                "description": f"성공적으로 {len(all_created_files)}개의 블로그 포스트를 생성했습니다."
            })
            return True, all_created_files
        else:
            self.send_notification({
                "title": "데이터 처리 실패",
                "description": "Markdown 파일 생성에 실패했습니다."
            })
            return False, []
    
    def commit_and_push_changes(self, created_files):
        """변경사항을 Git에 커밋하고 푸시"""
        self.send_notification({
            "title": "Git 업로드 시작",
            "description": "변경사항을 GitHub에 업로드 중..."
        })
        
        try:
            # Git add
            success, output = self.run_git_command("git add .")
            if not success:
                self.send_notification({
                    "title": "Git 업로드 실패",
                    "description": f"Git add 실패: {output}"
                })
                return False
            
            # Git commit
            commit_message = f"Add {len(created_files)} new AI news posts - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            success, output = self.run_git_command(f'git commit -m "{commit_message}"')
            if not success and "nothing to commit" not in output:
                self.send_notification({
                    "title": "Git 업로드 실패",
                    "description": f"Git commit 실패: {output}"
                })
                return False
            
            # Git push
            success, output = self.run_git_command("git push origin master")
            if not success:
                self.send_notification({
                    "title": "Git 업로드 실패",
                    "description": f"Git push 실패: {output}"
                })
                return False
            
            self.send_notification({
                "title": "Git 업로드 완료",
                "description": f"성공적으로 {len(created_files)}개의 포스트를 GitHub에 업로드했습니다."
            })
            return True
            
        except Exception as e:
            self.send_notification({
                "title": "Git 업로드 실패",
                "description": f"예외 발생: {str(e)}"
            })
            return False
    
    def send_blog_update_notification(self, created_files):
        """블로그 업데이트 알림 발송"""
        if hasattr(self, 'notifier') and self.notifier and self.notifier.service and created_files:
            # 파일명에서 제목 추출
            post_titles = []
            for file_path in created_files:
                filename = os.path.basename(file_path)
                # 날짜 부분 제거하고 제목 추출
                title_part = filename.replace('.md', '').split('-', 3)
                if len(title_part) > 3:
                    title = title_part[3].replace('-', ' ').title()
                    post_titles.append(title)
            
            self.send_notification({
                "title": f"블로그 업데이트 - {len(created_files)}개 새 포스트",
                "description": f"새로 추가된 포스트: {', '.join(post_titles[:3])}{'...' if len(post_titles) > 3 else ''}"
            })
    
    def run_full_automation(self):
        """전체 자동화 프로세스 실행"""
        print("🚀 AI News Blog 자동화 시작! (OAuth 버전)")
        self.send_notification({
            "title": "자동화 시스템 시작",
            "description": "전체 자동화 프로세스를 시작합니다."
        })
        
        # OAuth 인증 확인
        if not hasattr(self, 'notifier') or not self.notifier or not self.notifier.service:
            print("⚠️  Gmail OAuth 인증이 필요합니다.")
            print("scripts/gmail_oauth.py를 먼저 실행하여 OAuth 인증을 완료하세요.")
            return False
        
        # 1. Excel 파일 처리
        success, created_files = self.process_excel_files()
        if not success:
            return False
        
        if not created_files:
            self.send_notification({
                "title": "자동화 시스템 완료",
                "description": "새로 생성할 포스트가 없습니다."
            })
            return True
        
        # 2. Git 업로드
        success = self.commit_and_push_changes(created_files)
        if not success:
            return False
        
        # 3. 블로그 업데이트 알림
        self.send_blog_update_notification(created_files)
        
        # 4. 완료 알림
        self.send_notification({
            "title": "자동화 시스템 완료",
            "description": f"""전체 자동화 프로세스가 완료되었습니다! 🎉

📊 처리된 포스트: {len(created_files)}개
🌐 블로그 주소: https://winterkim-bot.github.io/sans
🔗 GitHub 저장소: https://github.com/winterkim-bot/sans

약 5-10분 후 GitHub Pages에서 업데이트된 블로그를 확인할 수 있습니다."""
        })
        
        print("✅ 자동화 완료!")
        return True

def main():
    """메인 함수"""
    automation = BlogAutomationOAuth()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "process":
            # Excel 파일만 처리
            success, files = automation.process_excel_files()
            if success:
                print(f"✅ {len(files)}개 파일 생성 완료")
            else:
                print("❌ 파일 처리 실패")
                
        elif command == "push":
            # Git 푸시만 실행
            files = glob.glob("_posts/*.md")
            success = automation.commit_and_push_changes(files)
            if success:
                print("✅ Git 푸시 완료")
            else:
                print("❌ Git 푸시 실패")
                
        elif command == "test-email":
            # 이메일 테스트
            automation.send_notification({
                "title": "OAuth 이메일 테스트",
                "description": "Gmail OAuth 시스템이 정상적으로 작동합니다! 🎉"
            })
            
        elif command == "setup-oauth":
            # OAuth 설정
            print("OAuth 설정을 시작합니다...")
            from gmail_oauth import setup_oauth_config
            setup_oauth_config()
            
        else:
            print("사용법: python3 main_automation_oauth.py [process|push|test-email|setup-oauth]")
    else:
        # 전체 자동화 실행
        automation.run_full_automation()

if __name__ == "__main__":
    main() 