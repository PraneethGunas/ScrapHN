from twilio.rest import Client

from bs4 import BeautifulSoup
import requests

res = requests.get("https://news.ycombinator.com/")

soup = BeautifulSoup(res.content, "lxml")
# print (soup.prettify())
keyWords = ["python","google","whatsapp","project"]
hmm = "HNHNHNHNHNHNHNHNHNHN\n"
scoreData = soup.find_all("span",{"class": "score"})

for d in scoreData:

    scoreId = d['id'].replace("score_","")
    link = soup.find("tr",{"id": scoreId})
    # print(scoreId)
    score = d.text
    i = score.find(" ")
    if int(score[:i]) > 200:
        
        hmm+=(link.text+"\n"+score)
        a = link.find("a",{"class","storylink"})
        hmm+=("\n"+a['href']+"\n")


def msg_mom_and_dad(event=None, context=None):

    # get your sid and auth token from twilio
    twilio_sid = 'AC84fe5628e43a547fe53fd1349dbff74e'
    auth_token = '6763d5cd72d0eb0238d7ac220e4f6dde'

    whatsapp_client = Client(twilio_sid, auth_token)

    # keep adding contacts to this dict to send
    # them the message
    contact_directory = {'Gunas':'+919901688282'}

    for key, value in contact_directory.items():
        msg_loved_ones = whatsapp_client.messages.create(
                body = hmm,
                from_= 'whatsapp:+14155238886',
                to='whatsapp:' + value,
            )

        if(msg_loved_ones.sid):
            print("Success!")

msg_mom_and_dad();
