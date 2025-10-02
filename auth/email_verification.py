import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "bsftraders4@gmail.com"
SMTP_PASS = "wxyqclckplvugusx" 

def generate_code() -> str:
    return str(random.randint(100000, 999999))

def send_email(to_email: str, code: str):
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding:20px;">
        <div style="max-width:600px; margin:auto; background:#fff; border-radius:8px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color:#333;">Подтверждение email</h2>
          <p>Здравствуйте!</p>
          <p>Ваш код подтверждения:</p>
          <div style="font-size:24px; font-weight:bold; color:#2c7be5; margin:20px 0;">
            {code}
          </div>
          <p>Код действителен в течение <b>10 минут</b>.</p>
          <p style="color:#777;">Если вы не запрашивали подтверждение, просто проигнорируйте это письмо.</p>
          <hr style="margin:20px 0;"/>
          <p style="font-size:12px; color:#aaa;">W3School Platform</p>
        </div>
      </body>
    </html>
    """

    # Формируем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Подтверждение email"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    # Добавляем HTML‑контент
    msg.attach(MIMEText(html_content, "html"))

    # Отправляем через Gmail SMTP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
