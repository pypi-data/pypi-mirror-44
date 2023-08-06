from vkeasybot import Decorators, DecoratorSearch


class CallBack(Decorators, DecoratorSearch):
    
    def __init__(self, vk, confirmation_token):
        super().__init__(vk=vk, confirmation_token=confirmation_token)
