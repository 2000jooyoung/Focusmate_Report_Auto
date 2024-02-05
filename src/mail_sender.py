import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_mail(subject, body, email, attachments=[]):
    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for attachment in attachments:
        with open(attachment, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition", "attachment", filename="file.pdf"
            )
            msg.attach(pdf_attachment)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "2000jooyoung@gmail.com"
    smtp_password = "upjb xwwf xavv drvw"  # my secret

    # Create a connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to your email account
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(smtp_username, email, msg.as_string())

    # Quit the server
    server.quit()
