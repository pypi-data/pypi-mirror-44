"""

coding: utf-8

author Ilya001
author email ilja.sonin2018@yandex.ru
author github https://github.com/Ilya001

python3.5+

"""
from threading import Thread
from enum import Enum
import requests
import json

from vkeasybot import Decorators, DecoratorSearch


class Event_list(list):

    class Operation(Enum):
        APPEND = 1
        REMOVE = 2

    def __init__(self,  *args, **kwargs):
        super(Event_list, self).__init__(*args, **kwargs)
        self.callbacks = []

    def add_callback(self, function):
        self.callbacks.append(function)

    def remove_callback(self, function):
        self.callbacks.remove(function)

    def append(self, value):
        super(Event_list, self).append(value)
        for callback in self.callbacks:
            callback(self.Operation.APPEND, value)

    def remove(self, value):
        super(Event_list, self).remove(value)
        for callback in self.callbacks:
            callback(self.Operation.REMOVE, value)


class EventTracking(DecoratorSearch):

    def __init__(self, event_list, decorators, vk):
        self.event_list = event_list
        self.decorators = decorators
        super().__init__(vk=vk)

    def _element(self, operation, event):
        if operation == self.event_list.Operation.APPEND:
            if event == None:
                self.event_list.remove(event)
            else:
                try:
                    self.start_search_decorate(event_object=event[0], decorators=self.decorators)
                except IndexError:
                    pass
                self.event_list.remove(event)

    def check_event(self):
        self.event_list.add_callback(self._element)


class LongPoll(Decorators):
    
    def __init__(self, vk, group_id):
        self.event_list = Event_list()
        super().__init__(vk=vk, group_id=group_id)

    def _get_server(self, ts=True):
        data = {'group_id': self.group_id}
        response = self.vk.vkmethod('groups.getLongPollServer', data)
        self.key = response['response']['key']
        self.server = response['response']['server']
        
        print('VK server received')

        if ts:
            self.ts = response['response']['ts']

        return {'server': self.server, 'key': self.key, 'ts': self.ts}

    def _connect_server(self):
        while True:
            response = requests.get("{}?act=a_check&key={}&ts={}&wait=25".format(self.server, self.key, self.ts))   
            response = json.loads(response.text)
            
            if 'failed' not in response:
                self.ts = response['ts']
                print("\nNew event\n{}".format(response))
                self.event_list.append(response['updates'])
                    
            elif response['failed'] == 1:
                self.ts = response['ts']

            elif response['failed'] == 2:
                self._get_server(ts=False)

            elif response['failed'] == 3:
                self._get_server()

    def start_listen(self):
        self._get_server()
        Thread(target=EventTracking(self.event_list, self.decorators, self.vk).check_event()).start()
        Thread(target=self._connect_server()).start()