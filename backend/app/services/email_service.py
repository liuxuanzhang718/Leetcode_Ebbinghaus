import emails
from typing import List
from datetime import datetime
from ..models.models import Problem, User
from ..core.config import settings

class EmailService:
    @staticmethod
    def create_review_email_html(problems: List[Problem], user: User) -> str:
        """Create HTML content for review reminder email."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .problem-card {{
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #f9f9f9;
                }}
                .difficulty {{
                    padding: 3px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    color: white;
                    display: inline-block;
                    margin-right: 10px;
                }}
                .Easy {{ background-color: #00af9b; }}
                .Medium {{ background-color: #ffb800; }}
                .Hard {{ background-color: #ff2d55; }}
                .progress {{
                    margin-top: 10px;
                    color: #666;
                }}
                .button {{
                    display: inline-block;
                    padding: 8px 15px;
                    margin: 5px;
                    border-radius: 4px;
                    text-decoration: none;
                    color: white;
                }}
                .complete {{ background-color: #4CAF50; }}
                .postpone {{ background-color: #2196F3; }}
            </style>
        </head>
        <body>
            <h2>📅 LeetCode Review Reminder - {today}</h2>
            <p>Here are your problems for review today:</p>
        """

        for problem in problems:
            difficulty_class = problem.difficulty.value
            stage_progress = f"Stage {problem.stage + 1}/5"
            problem_url = f"https://leetcode.com/problems/{problem.title.lower().replace(' ', '-')}/"
            
            html += f"""
            <div class="problem-card">
                <span class="difficulty {difficulty_class}">{difficulty_class}</span>
                <a href="{problem_url}" style="text-decoration: none; color: #1a1a1a;">
                    #{problem.leetcode_number} {problem.title}
                </a>
                <div class="progress">
                    <span>{stage_progress}</span>
                    <div style="background-color: #eee; height: 5px; border-radius: 3px; margin-top: 5px;">
                        <div style="background-color: #4CAF50; height: 100%; width: {(problem.stage + 1) * 20}%; border-radius: 3px;"></div>
                    </div>
                </div>
                <div style="margin-top: 10px;">
                    <a href="{settings.API_URL}/reviews/{problem.problem_id}/complete" class="button complete">✅ Mark Complete</a>
                    <a href="{settings.API_URL}/reviews/{problem.problem_id}/postpone" class="button postpone">⏰ Postpone</a>
                </div>
            </div>
            """

        html += """
            <p style="color: #666; margin-top: 20px;">
                Keep up the great work! Regular review is key to mastering algorithms.
            </p>
        </body>
        </html>
        """
        
        return html

    @staticmethod
    def send_review_reminder(user: User, problems: List[Problem]) -> bool:
        """Send review reminder email to user."""
        try:
            html_content = EmailService.create_review_email_html(problems, user)
            
            message = emails.html(
                html=html_content,
                subject=f"LeetCode Review Reminder - {datetime.now().strftime('%Y-%m-%d')}",
                mail_from=(settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_ADDRESS)
            )

            response = message.send(
                to=user.email,
                smtp={
                    "host": settings.SMTP_HOST,
                    "port": settings.SMTP_PORT,
                    "user": settings.SMTP_USER,
                    "password": settings.SMTP_PASSWORD,
                    "tls": True,
                }
            )

            return response.status_code == 250
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 