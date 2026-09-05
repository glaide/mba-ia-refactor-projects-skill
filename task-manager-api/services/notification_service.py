import os

from utils.datetime_utils import utc_now


class NotificationService:
    def __init__(self):
        self.notifications = []
        self.email_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.email_port = int(os.environ.get("SMTP_PORT", "587"))
        self.email_user = os.environ.get("SMTP_USER", "")
        self.email_password = os.environ.get("SMTP_PASSWORD", "")

    def send_email(self, to, subject, body):
        if not self.email_user or not self.email_password:
            print(f"[NOTIFY] Email skipped (no SMTP config): {subject} -> {to}")
            return False
        try:
            import smtplib
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.email_user, to, message)
            server.quit()
            return True
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False

    def notify_task_assigned(self, user, task):
        subject = f"Nova task atribuída: {task.title}"
        body = f"Olá {user.name},\n\nA task '{task.title}' foi atribuída a você."
        self.send_email(user.email, subject, body)
        self.notifications.append({
            'type': 'task_assigned',
            'user_id': user.id,
            'task_id': task.id,
            'timestamp': utc_now(),
        })

    def notify_task_overdue(self, user, task):
        subject = f"Task atrasada: {task.title}"
        body = f"Olá {user.name},\n\nA task '{task.title}' está atrasada!"
        self.send_email(user.email, subject, body)

    def get_notifications(self, user_id):
        return [n for n in self.notifications if n['user_id'] == user_id]
