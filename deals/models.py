import csv

from django.db import models
from django.db.models import Sum


class UploadModel(models.Model):
    deals = models.FileField(upload_to='uploads/')


class DealModel(models.Model):
    customer = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    total = models.FloatField()
    quantity = models.IntegerField()
    date = models.CharField(max_length=50)

    def __str__(self):
        return self.customer

    @staticmethod
    def load_to_database(filename):
        data = csv.reader(open(filename), delimiter=',')
        for row in data:
            if row[0] != 'customer':
                DealModel.objects.create(customer=row[0], item=row[1],
                                         total=row[2], quantity=row[3], date=row[4])

    @staticmethod
    def sample():
        # выборка топ-5 клиентов по тратам
        top_customers = DealModel.objects.values('customer').distinct().annotate(spent_money=Sum('total')).order_by(
            '-spent_money')[:5]
        # только имена клиентов с максимальными тратами
        top_customers_list = top_customers.values('customer')
        # список всех камней топ-5 клиентов
        gems = DealModel.objects.filter(customer__in=top_customers_list).values('item').distinct()
        result = []
        for customer in top_customers:
            spent_money = customer['spent_money']
            customer_name = customer['customer']
            gems_without_customer = gems.exclude(customer=customer_name)
            customer_gems = gems.filter(customer=customer_name)
            sample_gems = gems_without_customer.filter(item__in=customer_gems).values_list('item', flat=True)
            data = {'username': customer_name,
                    'spent_money': spent_money,
                    'gems': list(sample_gems)}
            result.append(data)
        return result
