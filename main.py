from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

def send_email(to_email: str, subject: str, message: str):
    try:
        # SMTP server configuration
        smtp_server = "smtp.hostinger.com"
        smtp_port = 465
        smtp_user = "support@edutechnica.id"
        smtp_password = "Temporary999-@"

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@app.post("/send-email/")
async def send_email_endpoint(email: EmailSchema):
    send_email(email.email, email.subject, email.message)
    return {"message": "Email sent successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
