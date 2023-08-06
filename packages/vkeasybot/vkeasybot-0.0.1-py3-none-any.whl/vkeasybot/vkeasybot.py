"""

coding: utf-8

author Ilya001
author email ilja.sonin2018@yandex.ru
author github https://github.com/Ilya001

python3.5+

"""
import requests
import random
import json


class VkEasyBot:

    recommended_api_version = 5.92

    def __init__(self, **kwargs):
        self.token = kwargs.get('token', None)
        self.v = kwargs.get('v', None)
        self._method = kwargs.get('method', None)

    def __getattr__(self, method):
        return VkEasyBot(token=self.token,
                        v=self.v,
                        method = (self._method + '.' if self._method else '') + method)

    def __call__(self, **kwargs):
        return self.vkmethod(self._method, kwargs)

    def vkmethod(self, method, data):
        token = getattr(self, "token", None)
        v = getattr(self, "v", None)

        if v is None:
            v = self.recommended_api_version

        if 'v' not in data:
            data['v'] = v

        if 'token' not in data:
            if 'access_token' not in data:
                if token:
                    data['access_token'] = token
        
        data['random_id'] = random.randint(1, 1000000)
        response = requests.post("https://api.vk.com/method/{}".format(method), data)
        
        if 'error' in response.text:
            errors = json.loads(response.text)
            print(errors)
        elif response.ok:
            return json.loads(response.text)
        else:
            return json.loads(response.text)


class Decorators:

    decorators = []

    def __init__(self, **kwargs):
        self._method = kwargs.get('method', None)
        for key, value in kwargs.items():
            self.__setattr__(key.lower(), value)

    def __getattr__(self, method):
        return Decorators(method=(self._method + '.' if self._method else '') + method)

    def __call__(self, function):
        self.decorators.append({'type': self._method, 'function': function})


class Event(VkEasyBot):

    attachments = None
    body = None
    text = None
    user_id = None
    from_id = None
    title = None

    def __init__(self, token, v):
        super().__init__(token=token, v=v)


def _decorate(function):

    def _decorated_function(vk, event):
        ev = Event(vk.token, vk.v)
        setattr(ev, 'event', event)
        for key, value in event.items():
            setattr(ev, key, value)
        message = function(ev)
        del ev
        if type(message).__name__ == "str" and event.get('from_id', None):
            vk.messages.send(user_id=event['from_id'], message=message)
        if type(message).__name__ == "list" and event.get('from_id', None):
            vk.messages.send(user_id=event['from_id'], message=message[random.randint(1, len(message))-1])
        return 'ok'

    return _decorated_function


class DecoratorSearch:

    def __init__(self, **kwargs):
        self.vk = kwargs.get('vk', None)
        self.confirmation_token = kwargs.get('confirmation_token', None)

    def _create_decr(self, function, event):
        function = _decorate(function)
        return function(self.vk, event)
    
    def start_search_decorate(self, event_object, decorators):
        typ = event_object.get('type', None)
        event = event_object.get('object', None)
        if typ == 'confirmation':
            if self.confirmation_token:
                return self.confirmation_token
        for decr in decorators:
            if decr['type'] == typ:
                return self._create_decr(decr['function'], event)
        return 'ok'
