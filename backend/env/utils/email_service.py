import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os



SENDER_EMAIL = "chinmaykashyapcs@gmail.com"

# ⚠️ IMPORTANT: Replace with your Gmail App Password
SENDER_PASSWORD = "ebvz vaac ljlf vevy"


def send_email(to_email, subject, body):

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            # 🔥 FIX HERE
            server.sendmail(
                SENDER_EMAIL,
                to_email,
                msg.as_string()
            )

        print(f"[EMAIL SENT] → {to_email}")

    except Exception as e:
        print(f"[EMAIL ERROR] → {to_email} → {str(e)}")


def send_email_with_attachment(to_email, subject, body, file_path):

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(
                SENDER_EMAIL,
                to_email,
                msg.as_string()
            )

        print(f"[EMAIL WITH ATTACHMENT SENT] → {to_email}")

    except Exception as e:
        print(f"[EMAIL ERROR] → {to_email} → {str(e)}")
def send_email_with_pdf(to_email, subject, body, pdf_path):

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Attach PDF
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_part = MIMEApplication(f.read(), _subtype="pdf")
                pdf_part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(pdf_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(
                SENDER_EMAIL,
                to_email,
                msg.as_string()
            )

        print(f"[PDF EMAIL SENT] → {to_email}")

    except Exception as e:
        print(f"[EMAIL ERROR] → {to_email} → {str(e)}")