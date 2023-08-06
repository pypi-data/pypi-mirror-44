import requests
import random

__all__ = frozenset({'merchant'})


class Merchant:
    def __init__(self, user_id, key):
        self.key = key
        self.id = int(user_id)
        self.url = 'https://coin-without-bugs.vkforms.ru/merchant/'

    def get_payment_url(self, amount, payload=random.randint(-2000000000, 2000000000), free_amount=False):
        if free_amount:
            return 'vk.com/coin#m{id}_{sum}_{payload}_1'.format(id=self.id, sum=amount * 1000, payload=payload)
        else:
            return 'vk.com/coin#m{id}_{sum}_{payload}'.format(id=self.id, sum=amount * 1000, payload=payload)

    def get_transactions(self, tx, last_tx=None):
        if last_tx is None:
            transactions = requests.post(self.url + 'tx/',
                                         data={'merchantId': self.id, 'key': self.key, 'tx': tx})
        else:
            transactions = requests.post(self.url + 'tx/',
                                         data={'merchantId': self.id, 'key': self.key, 'tx': tx, 'lastTx': last_tx})
        return transactions.json()

    def send(self, amount, to_id):
        transactions = requests.post(self.url + 'send/',
                                     data={'merchantId': self.id, 'key': self.key, 'toId': to_id,
                                           'amount': amount * 1000})
        return transactions.json()
