import smtplib
from email.mime.text import MIMEText
from app.config.settings import settings


def send_email(to: str, subject: str, message: str):
    """
    Envía un email usando SMTP.
    Requiere EMAIL_USER y EMAIL_PASS en las variables de entorno.
    Si no están configuradas, solo imprime en consola (modo desarrollo).
    """
    if not settings.EMAIL_USER or not settings.EMAIL_PASS:
        print(f"[EMAIL] Para: {to} | Asunto: {subject} | Mensaje: {message}")
        return

    try:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_USER
        msg["To"] = to

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.sendmail(settings.EMAIL_USER, to, msg.as_string())

        print(f"[EMAIL] Enviado correctamente a {to}")

    except Exception as e:
        print(f"[EMAIL] Error al enviar email: {e}")
