from accounts.models import Purchase
import datetime

def check_payments():
    due_payments = Purchase.objects.filter(date= datetime.date.today(), upcoming=True)
    for p in due_payments: 
        # pay this payment and create the a new future payment in the billing cycle
        p.upcoming = False
        next_pay = Purchase.objects.create(user=p.user, purchase_name=p.purchase_name, price=p.price, 
                                date=datetime.date.today() + p.user.subscription.payment_interval, 
                                card=p.card, upcoming=True)
        p.save()
        next_pay.save()