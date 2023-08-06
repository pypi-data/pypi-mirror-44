import requests
import json
from pubnub import Pubnub
from haikunator import Haikunator

publish_key = 'pub-0f6a95b6-4f0e-4ae1-ac1c-454dab230cb9'
subscribe_key = 'sub-6275b419-2334-11e2-a48a-45362bc1d0c2'
haikunator = Haikunator()

ENV = 'local'
HOSTNAME = 'https://ikuzo-backend.herokuapp.com/' if ENV == 'prod' else 'http://localhost:3000/'

class Ikuzo():
    def __init__(self, debug=False):
        self.pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key)
        self.debug = debug

    def callback(self, message):
        if self.debug: print(message)

    def connect(self, message):
        print("CONNECTED to {}".format(message))
        channel = message.replace('-input', '')
        print("Go to {}apis/{} to access your API".format(HOSTNAME, channel))
        
    def reconnect(self, message):
        print("RECONNECTED")
    
    def disconnect(self, message):
        print("DISCONNECTED")
    
    def noop(self, input):
        return "haha this is the translated text"

    def launch(self, fn, title=None, input_type='text', output_type='text'):
        # request backend for hash
        haiku = haikunator.haikunate()
        json_body = {
            'title': title or haiku,
            'channel_id': haiku,
            'input_type': 'text',
            'output_type': 'text'
        }

        r = requests.post(HOSTNAME + 'apis.json', json=json_body, headers={'Content-type': 'application/json'})
        response = r.json()
        if self.debug: print(response)

        input_channel_id = response['channel_id'] + '-input'
        output_channel_id = response['channel_id'] + '-output'

        def subscribe_callback(message, channel):
            print("RECEIVED INPUT from {}:".format(channel))
            print(message)
            
            # run function when input is retrieved
            output = fn(message['input'])
            msg = {'output': output}

            print("SENDING OUTPUT:")
            print(msg)

            self.pubnub.publish(output_channel_id, msg, callback=self.callback, error=self.callback)
            
        # start listening to pubnub input
        self.pubnub.subscribe(channels=input_channel_id, callback=subscribe_callback, error=subscribe_callback,
                    connect=self.connect, reconnect=self.reconnect, disconnect=self.disconnect)
        
        # kill when done
        return