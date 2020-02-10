from django.db import models

import csv


class UploadModel(models.Model):
    deals = models.FileField(verbose_name='csv-файл', upload_to='uploads/')

    def __str__(self):
        return self.deals


class DealModel(models.Model):
    customer = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    total = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date = models.CharField(max_length=50)

    def import_to_base(csv_name):
        data = csv.reader(open(csv_name), delimiter=',')
        dates = DealModel.objects.values_list('date', flat=True)
        for row in data:
            if row[0] != 'customer':
                jewels = DealModel(customer=row[0], item=row[1],
                                   total=row[2], quantity=row[3], date=row[4])
                if jewels.date not in dates:
                    jewels.save()


class ResultModel(models.Model):
    username = models.CharField(max_length=50)
    spent_money = models.PositiveIntegerField()
    gems = models.CharField(max_length=100)

    class Meta:
        ordering = ('-spent_money',)

    def make_all():
        records = DealModel.objects.all()
        users = []
        for element in records:
            if element.customer not in users:
                spent_money = 0
                gems_lst = []
                for record in records:
                    if record.customer == element.customer:
                        spent_money += record.total
                        if record.item not in gems_lst:
                            gems_lst.append(record.item)
                ResultModel.objects.create(username=element.customer,
                                           spent_money=spent_money,
                                           gems=gems_lst)
                users.append(element.customer)

    def give_gems():
        important_customers = ResultModel.objects.all()[:5]
        big_lst_gems = []
        for customer in important_customers:
            lst_gems = []
            for record in DealModel.objects.filter(customer=customer.username):
                if record.item not in lst_gems:
                    lst_gems.append(record.item)
            big_lst_gems += lst_gems
        replay_gems = []
        for gem in big_lst_gems:
            if big_lst_gems.count(gem) != 1:
                replay_gems.append(gem)
        big_lst_gems = set(replay_gems)
        for customer in important_customers:
            customer_gems = []
            for record in DealModel.objects.filter(customer=customer.username):
                if record.item in big_lst_gems:
                    if record.item not in customer_gems:
                        customer_gems.append(record.item)
            obj = ResultModel.objects.get(username=customer.username)
            obj.gems = customer_gems
            obj.save()
