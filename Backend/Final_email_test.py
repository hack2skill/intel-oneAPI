from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter()
#templates = Jinja2Templates(directory="templates")

MAILGUN_API_KEY = ""
MAILGUN_DOMAIN = ""



@router.post("/email")
def send_email_route(receiver_email: str = Form(...), subject: str = Form(...), message: str = Form(...)):
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    sender_email="angeloantu@gmail.com"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": sender_email,
        "to": receiver_email,
        "subject": subject,
        "text": message
    }

    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        print("Email sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the email: {str(e)}")


