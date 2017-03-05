import requests
import re
import string
from flask import Flask, request, Response
from textblob import TextBlob
my_bot_name = 'gu_bot'  # e.g. zac_bot
my_slack_username = 'xgu10'  # e.g. zac.wentzell
IP_Adrees = '52.36.225.157'

app = Flask(__name__)

# FILL THESE IN WITH YOUR INFO


slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@app.route('/slack', methods=['POST'])
def inbound():


    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':robot_face:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'zac.wentzell','xgu10']:
        # Your code for the assignment must stay within this if statement

        # A sample response:
        if text[0:20] == "&lt;BOTS_RESPOND&gt;":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Hello, my name is ' + my_bot_name + '. I belong to ' + my_slack_username + '. I live at '+ IP_Adrees
            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

        if text[0:36]=="&lt;WHAT'S_THE_WEATHER_LIKE_AT&gt;: ":
            key='AIzaSyAjOFryzSVOEoYlxOb3alt9KF_MwcQo2hE'
            text=text[36:]
            url='https://maps.googleapis.com/maps/api/geocode/json?address=' + text +'&key=' + key
            response = requests.get(url)
            result = response.json()
            lat=result['results'][0]['geometry']['location']['lat']
            lng=result['results'][0]['geometry']['location']['lng']
            link ='http://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(lng)+'&appid=fd38d62aa4fe1a03d86eee91fcd69f6e'
            rg=requests.get(link)
            data=rg.json()
            tem_K = data['list'][0]['main']['temp']
            tem_f = round((tem_K-273.15)*1.8+32,2)
            humidity=data['list'][0]['main']['humidity']
            weather=data['list'][0]['weather'][0]['description']
            wind=data['list'][0]['wind']['speed']
            img='https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(lng)+'&zoom=13&size=400x400&key=AIzaSyBLxmTjkdETZoEDOtP6pfBLfe6jJU8hT0A'
           #day2_tem_k=data['list'][6]['main']['temp']
           # day2_tem_f=round((day2_tem_k-273.15)*1.8+32,2)
           # day2_humidity=data['list'][6]['main']['humidity']
           # day2_weather=data['list'][6]['weather'][0]['description']
           # day2_wind=data['list'][0]['wind']['speed']


            response={
                "username":'gxf_bot',
                "icon_emoji":'robot_face',
                "attachments": [
                {"pretext": "weather forecast",
                 "fields": [
                     {"title": "Temperature",
                      "value": tem_f,
                      "short":True},
                     {"title": "Weather",
                      "value": weather,
                      "short": True},
                     {"title": "Humidity",
                      "value": humidity,
                      "short": True},
                     {"title": "Wind",
                      "value": wind,
                      "short": True}],
                  "image_url":img}]}


            r = requests.post(slack_inbound_url, json=response)




        if text[0:33]=="&lt;I_NEED_HELP_WITH_CODING&gt;: ":
            if '[' and ']' in text:
                tag = re.findall('(?<=\[)\w+', text)
                tag_url="%3B".join(tag)
                text = re.sub('(?<=\[)\w+', '', text)
                text_elim=text.replace('[','')
                text_elim2=text_elim.replace(']','')
                question=text_elim2.replace(' ','%20')
                url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' + question + '&accepted=True&closed=True&tagged='+tag_url+'&site=stackoverflow'
                response = requests.get(url)
                result = response.json()
                title = []
                link = []
                footer = []
                time = []
                for item in result['items'][0:5]:
                    title.append(item['title'])
                    link.append(item['link'])
                    footer.append(item['answer_count'])
                    time.append(item['creation_date'])


                response={
                "username":'gxf_bot',
                "icon_emoji":'robot_face',
                "attachments":[
                {"title":title[0],
                 "title_link":link[0],
                 "footer":footer[0],
                 "ts":time[0]},{"title":title[1],
                 "title_link":link[1],
                 "footer":footer[1],
                 "ts":time[1]},{"title":title[2],
                 "title_link":link[2],
                 "footer":footer[2],
                 "ts":time[2]},{"title":title[3],
                 "title_link":link[3],
                 "footer":footer[3],
                 "ts":time[3]},{"title":title[4],
                 "title_link":link[4],
                 "footer":footer[4],
                 "ts":time[4]}
                ]}
                r = requests.post(slack_inbound_url, json=response)




            else:
                question=text[33:].replace(' ','%20')
                url='https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q='+question+'&accepted=True&closed=True&site=stackoverflow'
                response = requests.get(url)
                result = response.json()
                title = []
                link = []
                footer = []
                time = []
                for item in result['items'][0:5]:
                    title.append(item['title'])
                    link.append(item['link'])
                    footer.append(item['answer_count'])
                    time.append(item['creation_date'])


                response={
                "username":'gxf_bot',
                "icon_emoji":'robot_face',
                "attachments":[
                {"title":title[0],
                 "title_link":link[0],
                 "footer":footer[0],
                 "ts":time[0]},{"title":title[1],
                 "title_link":link[1],
                 "footer":footer[1],
                 "ts":time[1]},{"title":title[2],
                 "title_link":link[2],
                 "footer":footer[2],
                 "ts":time[2]},{"title":title[3],
                 "title_link":link[3],
                 "footer":footer[3],
                 "ts":time[3]},{"title":title[4],
                 "title_link":link[4],
                 "footer":footer[4],
                 "ts":time[4]}
                ]}
                r = requests.post(slack_inbound_url, json=response)




    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@app.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=41953)
