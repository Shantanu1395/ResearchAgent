"""Email notification tools for sending reports."""

import os
import json
import logging
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Send email notifications with reports."""

    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None,
    ):
        """Initialize email notifier.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            sender_email: Sender email address (from env if not provided)
            sender_password: Sender email password (from env if not provided)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email or os.getenv("EMAIL_SENDER")
        self.sender_password = sender_password or os.getenv("EMAIL_PASSWORD")
        self.is_configured = bool(self.sender_email and self.sender_password)

    def send_report_email(
        self,
        recipient_emails: List[str],
        run_id: str,
        report_dir: Path,
        startup_count: int,
        tier_breakdown: Dict[str, int],
        subject_prefix: str = "Startup Research Report",
    ) -> bool:
        """Send report email with attachments.
        
        Args:
            recipient_emails: List of recipient email addresses
            run_id: Run ID for the report
            report_dir: Directory containing report files
            startup_count: Total startups found
            tier_breakdown: Dictionary with tier counts
            subject_prefix: Email subject prefix
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            logger.warning("⚠️  Email not configured. Set EMAIL_SENDER and EMAIL_PASSWORD in .env")
            return False

        try:
            # Create email message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"{subject_prefix} - {run_id}"
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(recipient_emails)

            # Create HTML body
            html_body = self._create_html_body(
                run_id, startup_count, tier_breakdown
            )
            msg.attach(MIMEText(html_body, "html"))

            # Attach report files
            self._attach_files(msg, report_dir)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"✅ Email sent to {', '.join(recipient_emails)}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False

    def _create_html_body(
        self, run_id: str, startup_count: int, tier_breakdown: Dict[str, int]
    ) -> str:
        """Create HTML email body."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tier_html = "".join([
            f"<li><strong>{tier}:</strong> {count} startups</li>"
            for tier, count in tier_breakdown.items()
        ])

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">
                        📊 Startup Research Report
                    </h2>
                    
                    <p><strong>Run ID:</strong> {run_id}</p>
                    <p><strong>Generated:</strong> {timestamp}</p>
                    
                    <h3 style="color: #34495e; margin-top: 20px;">Summary</h3>
                    <ul style="background-color: #ecf0f1; padding: 15px 30px; border-radius: 5px;">
                        <li><strong>Total Startups Found:</strong> {startup_count}</li>
                        {tier_html}
                    </ul>
                    
                    <h3 style="color: #34495e; margin-top: 20px;">Report Files</h3>
                    <p>The following files are attached:</p>
                    <ul>
                        <li>agents_summary.json - Summary of all agents</li>
                        <li>Individual agent reports (JSON)</li>
                    </ul>
                    
                    <h3 style="color: #34495e; margin-top: 20px;">Next Steps</h3>
                    <ol>
                        <li>Review the attached reports</li>
                        <li>Check the database for detailed startup information</li>
                        <li>Analyze market opportunities by tier</li>
                    </ol>
                    
                    <hr style="border: none; border-top: 1px solid #bdc3c7; margin: 20px 0;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        This is an automated email from the Startup Research Agent.
                        Please do not reply to this email.
                    </p>
                </div>
            </body>
        </html>
        """
        return html

    def _attach_files(self, msg: MIMEMultipart, report_dir: Path) -> None:
        """Attach report files to email."""
        if not report_dir.exists():
            logger.warning(f"Report directory not found: {report_dir}")
            return

        # Attach JSON files
        for json_file in report_dir.glob("*.json"):
            try:
                with open(json_file, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {json_file.name}",
                    )
                    msg.attach(part)
                logger.debug(f"Attached: {json_file.name}")
            except Exception as e:
                logger.warning(f"Failed to attach {json_file.name}: {e}")


def send_startup_report_email(
    recipient_emails: List[str],
    run_id: str,
    report_dir: Path,
    startup_count: int,
    tier_breakdown: Dict[str, int],
) -> bool:
    """Convenience function to send startup report email.
    
    Args:
        recipient_emails: List of recipient email addresses
        run_id: Run ID for the report
        report_dir: Directory containing report files
        startup_count: Total startups found
        tier_breakdown: Dictionary with tier counts
        
    Returns:
        True if email sent successfully, False otherwise
    """
    notifier = EmailNotifier()
    return notifier.send_report_email(
        recipient_emails=recipient_emails,
        run_id=run_id,
        report_dir=report_dir,
        startup_count=startup_count,
        tier_breakdown=tier_breakdown,
    )

