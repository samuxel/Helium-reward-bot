
import json
import time
from datetime import datetime
import py_imessage
import pytz
import requests


#checks if number of rewards has changed
def check_reward (address):
    t_type = 'rewards_v2'
    url='https://api.helium.io/v1/hotspots/'+ address + '/activity/count'+'?'+ 'filter_types='+ t_type 
    html = requests.get(url,headers=headers)
    site_json=json.loads(html.text)
    data = site_json.get('data')
    reward_number = int(data.get('rewards_v2'))
    return reward_number

    
#functions for time 
def now ():
    nowe = datetime.now()
    dt_object = nowe.astimezone(pytz.timezone('Europe/Berlin')).strftime('%H:%M')
    return dt_object

def get_time (timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    #change timezone if needed
    dt_object = dt_object.astimezone(pytz.timezone('Europe/Berlin')).strftime('%H:%M')
    
    return dt_object

#functions for sending the message via imessage
def send(message):
    time.sleep(10)
    
    py_imessage.send([''], message) #enter icloud emailadress or phone number you want to be notified on
    time.sleep(10)
    #time.sleep(5)
    
    
def reward_message(r_type,r_time,r_amount):
    message = 'new reward!' ' | Amount: ' +r_amount + ' USD | ' + 'Type: ' + r_type.lower() + ' | ' 'time: ' + r_time +'oclock |' 
    print('Log: ' + message)
    send(message)

#function for logging activity
def start_message():
    dt_object = now()
    message2 = 'The bot has been started at ' + dt_object + ' !'
    print('Log: ' + message2)
    message2 = 'you will be notified here once the first reward has been made'
    print('Log: ' + message2)

def in_timestamp(timestamp):
    start=timestamp.rfind('T')+1
    end= timestamp.find('.')
    result= timestamp[start:end]
    return result

def get_reward(address):
    time = r"min_time=2022-01-16"
    url = 'https://api.helium.io/v1/hotspots/' + address + '/rewards' +'?'+ time
    html = requests.get(url,headers=headers)
    site_json=json.loads(html.text)
    data = site_json.get('data')
    type = data[0]['type']
    amount= data[0]['amount']
    timestamp = data[0]['timestamp']
    timestamp =in_timestamp(timestamp)
    #the current Helium price is to be made dynamic in v2
    usdvalue=20
    amount = (amount*0.00000001)*usdvalue
    amount=str(round(amount,3))
    reward_message(type,timestamp,amount)
    

not_stopped = True
headers = {'User-Agent': ''} #request a custom user agent name from Helium for unlimited API requests
name = '' #enter your miners name
name = name.lower()
trueName = name.replace(" ", "-")
name = name.replace(" ", "_")
url = 'https://api.helium.io/v1/hotspots/name?search='+ name
html = requests.get(url,headers=headers)
site_json=json.loads(html.text)
data = site_json.get('data')

if data[0]['name'] != trueName:
    print ('No Miner found ')
else:
    start_message()
    minerObject = data[0]
    address= minerObject.get('address')
    rewards=check_reward(address)
    reward_number = rewards
    
    while not_stopped == True:
        rewards=check_reward(address)
        print(rewards)
        
        if reward_number < rewards:
            reward_number =  rewards
            transaction = get_reward(address)
        else:
            time.sleep(300)
            print('Log: Bot is still active at ' + now() + ' oclock')


    



