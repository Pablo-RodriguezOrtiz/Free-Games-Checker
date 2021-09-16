## Made with Python 3.9.7

# Import necesary modules.
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime

# Call API and get data.
free_games=f"https://www.gamerpower.com/api/giveaways?platform=pc"
data=requests.get(free_games)
pc_games=data.json()

# Read all the data and get important information.
Fullgame=""
Loot=""

# Create variables for today and 2 days ago.
now= datetime.datetime.now()
yesterday=now.date()-datetime.timedelta(days=1)

for i in range(len(pc_games)): #Loop to separate full games and DLC & Loot.
    date=datetime.date(int(pc_games[i]['published_date'][0:4]),int(pc_games[i]['published_date'][5:7]),int(pc_games[i]['published_date'][8:10]))
    if date > yesterday:
        if pc_games[i]['type']=="Full Game":
            Fullgame+=f"{pc_games[i]['title']}\n{pc_games[i]['description']}\nInstructions:\n{pc_games[i]['instructions']}\nURL: {pc_games[i]['open_giveaway']}\n\n"
        else:
            Loot+=f"{pc_games[i]['title']}\n{pc_games[i]['description']}\nInstructions:\n{pc_games[i]['instructions']}\nURL: {pc_games[i]['open_giveaway']}\n\n"

# Create message object instance.
msg = MIMEMultipart()
message=""

# Setup the parameters of the message.
password = "your_password"
msg['From'] = "your_mail"
msg['To'] = "to_mail"
msg['Subject'] = f"Free Games ({now.date()})"

def send_mail():
    # Add in the message body.
    msg.attach(MIMEText(message, 'plain'))

    # Create SMTP server.
    server = smtplib.SMTP('smtp.gmail.com: 587')
    
    server.starttls()
    
    # Login Credentials for sending the mail.
    server.login(msg['From'], password)
    
    
    # Send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()

# Setup message to send.
if Fullgame=="" and Loot=="":
    pass
elif Fullgame=="" and Loot!="":
    message=f"DLC & Loots:\n\n{Loot}"
    send_mail()
elif Fullgame!="" and Loot=="":
    message=f"Juegos completos:\n\n{Fullgame}"
    send_mail()
else:
    message=f"Juegos completos:\n\n{Fullgame}\nDLC y Loots:\n\n{Loot}"
    send_mail()
