import requests

from errors import handle_err

global mailgunConfig

def send_mail(recipientList, subject, content):
    try:
        data = requests.post(
            f"https://api.mailgun.net/v3/{ mailgunConfig['hostname'] }/messages",
            auth= ( "api", mailgunConfig["privateKey"] ),
            data={
                "from": f"Noreply <mailgun@{ mailgunConfig['hostname'] }>",
                "to": recipientList,
                "subject": subject,
                "text": content
            }
        )
        return [ data, None ]

    except Exception as e:
        return [ None, handle_err(e) ]