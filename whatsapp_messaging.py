from twilio.rest import Client

from bs4 import BeautifulSoup
import requests

import redis
r = redis.Redis(host = 'localhost', port = 6379)

res = requests.get("https://news.ycombinator.com/")

soup = BeautifulSoup(res.content, "lxml")

hmm = "YCOMBINATOR\n"

scoreData = soup.find_all("span",{"class": "score"})

for d in scoreData:

    scoreId = d['id'].replace("score_","")
    link = soup.find("tr",{"id": scoreId})
    # print(scoreId)
    score = d.text
    i = score.find(" ")
    if int(score[:i]) > 200:
        if r.get(d['id']) == None:
            r.set(d["id"], int(score[:i]), px = 4000000*24)
            hmm+=(link.text+"\n"+score)
            a = link.find("a",{"class","storylink"})
            hmm+=("\n"+a['href']+"\n")
        else:
            # print(r.get(d['id']))
            continue
if hmm == "YCOMBINATOR\n":
    hmm = "Nothing new yet!"


def msg_auto(event=None, context=None):

    # get your sid and auth token from twilio
    twilio_sid = '{your-sid}'
    auth_token = '{your-auth-token}'

    whatsapp_client = Client(twilio_sid, auth_token)

    # keep adding contacts to this dict to send
    # them the message
    contact_directory = {'Gunas':'{#phno}'}

    for key, value in contact_directory.items():
        msg_loved_ones = whatsapp_client.messages.create(
                body = hmm,
                from_= "whatsapp:{#twilo's-trial}",
                to='whatsapp:' + value,
            )

        if(msg_loved_ones.sid):
            print("Success!")

msg_auto();
