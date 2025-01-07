import __init__
from models.database import engine
from models.model import Payments, Subscription
from sqlmodel import Session, select
from datetime import date, datetime

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription
    
    def listAll(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
    
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    def _hasPay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.enterprise==subscription.enterprise)
            results = session.exec(statement).all()
            if self._hasPay(results):
                question = input('Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N: ')
                
                if not question.upper() == 'Y':
                    return
            
            pay = Payments(subscriptionId=subscription.id, date=date.today())
            session.add(pay)
            session.commit()

    def totalValue(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()

        total = 0
        for result in results:
            total += result.price

        return float(total)
    
    def _getLastTwelvesMonthsNative(self):
        today = datetime.now()
        year = today.year
        month = today.month
        lastTwelvesMonth = []
        for _ in range(12):
            lastTwelvesMonth.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return lastTwelvesMonth[::-1]

    def _getValuesForMonths(self, lastTwelvesMonths):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            valueForMonths = []
            for i in lastTwelvesMonths:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.price)
                valueForMonths.append(value)
            return valueForMonths
    
    def generateChart(self):
        lastTwelvesMonths = self._getLastTwelvesMonthsNative()
        valuesForMonths = self._getValuesForMonths(lastTwelvesMonths)
        last_12_months = list(map(lambda x: x[0], self._getLastTwelvesMonthsNative()))
        
        import matplotlib.pyplot as plt

        plt.plot(last_12_months, valuesForMonths)
        plt.show()

