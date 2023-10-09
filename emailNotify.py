import yagmail
# set your email and password
# please use App Password
email_address = "notifyearlierdate@gmail.com"
app_password = "gbcwsvegqstqihie"
# yes I know storing my password in plaintext in a python file is bad practice but this is a developer/throwaway email so whatever

#send_to = ["prestonwww@gmail.com", "kaito1410@gmail.com"]
send_to = ["kaito1410@gmail.com"]

def send_email(date_string, update_content):
    subject = 'Instagram weekly updates from Summary APP: ' + date_string
    # TODO: update to imbedded imagines into the email, but this may not be practical because of the sizes
    # and formatting for each image
    # consider adding a instagram link in the contents that will open instagram app and show the media instead
    content = [update_content]

    with yagmail.SMTP(email_address, app_password) as yag:
        yag.send(send_to, subject, content)
        print('Sent email successfully')