from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class ProductPrice(models.Model):
    code = models.ForeignKey(Product, on_delete=models.CASCADE, help_text='ForeinKey to Product code')
    price = models.PositiveIntegerField(help_text='Price of product in cents', blank=False, null=False)
    promo_date_start = models.DateField(help_text='date to apply the new price', blank=False, null=False)
    isActive = models.BooleanField(help_text='flag is the promo is enabled', default=False)
    isBlack_friday = models.BooleanField(help_text='flag if the price is black friday offer', default=False)

    class Meta:
        ordering = ('code',)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)
