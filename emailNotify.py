import yagmail
# set your email and password
# please use App Password
email_address = "notifyearlierdate@gmail.com"
app_password = "gbcwsvegqstqihie"

#send_to = ["prestonwww@gmail.com", "kaito1410@gmail.com"]
send_to = ["kaito1410@gmail.com"]

def send_email(date_string, update_content):
    subject = 'Instagram weekly updates from Summary APP: ' + date_string
    content = [update_content]

    with yagmail.SMTP(email_address, app_password) as yag:
        yag.send(send_to, subject, content)
        print('Sent email successfully')