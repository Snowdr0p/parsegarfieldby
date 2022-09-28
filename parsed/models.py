from django.db import models
from djmoney.models.fields import MoneyField


class Site(models.Model):
    name = models.CharField(max_length=30, verbose_name='название')
    url = models.URLField(verbose_name='URL-адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'сайт'
        verbose_name_plural = 'сайты'


class Animal(models.Model):
    type = models.CharField(max_length=20, verbose_name='вид')
    url = models.URLField(verbose_name='URL-адрес')
    site = models.ManyToManyField(Site)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'животное'
        verbose_name_plural = 'животные'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='название')
    url = models.URLField(verbose_name='URL-адрес')
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} для {self.animal.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=40, verbose_name='название')
    description = models.CharField(max_length=60, verbose_name='описание')
    image_url = models.URLField(verbose_name='URL-адрес изображения товара')
    amount = models.CharField(max_length=20, verbose_name='цена за')
    cost = MoneyField(max_digits=9, decimal_places=2, default_currency='BYN', verbose_name='цена')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.amount} {self.cost}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
