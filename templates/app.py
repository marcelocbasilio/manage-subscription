import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscriptionService = SubscriptionService(engine)

    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Sair
            ''')

            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self.addSubscription()
            elif choice == 2:
                self.deleteSubscription()
            elif choice == 3:
                self.totalValue()
            elif choice == 4:
                self.subscriptionService.generateChart()
                # TODO: Chamar o método pay na interface.
            else:
                break

    def addSubscription(self):
        enterprise = input('Empresa: ')
        site = input('Site: ')
        dateSignature = datetime.strptime(input('Data de assinatura: '), '%d/%m/%Y')
        price = Decimal(input('Valor: '))
        subscription = Subscription(enterprise=enterprise, site=site, dateSignature=dateSignature, price=price)
        self.subscriptionService.create(subscription)

    def deleteSubscription(self):
        subscriptions = self.subscriptionService.listAll()
        # TODO: Quando excluir a assinatura, excluir todos os pagamentos dela.
        print('Escolha qual assinatura deseja excluir?')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.enterprise}')

        choice = int(input('Escolha a assinatura: '))
        self.subscriptionService.delete(choice)
        print('Assinatura excluída com sucesso!')

    def totalValue(self):
        print(f'Seu valor total mensal em assinatura é: {self.subscriptionService.totalValue()}')

if __name__ == '__main__':
    UI().start()

    