import requests
from django.core.mail import send_mail
from core.settings import DEFAULT_FROM_EMAIL
from background_task import background

from .models import monitoringStock, historyMonitoring


def getListCompany():
    url = 'https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc'
    r = requests.get(url)
    listCompanys = r.json()

    return listCompanys['stocks']


@background(schedule=0)
def strockMonitoringService(stock):
    stockModel = monitoringStock.objects.get(stock=stock)

    url = 'https://brapi.dev/api/quote/%s?range=1d&interval=1d&fundamental=false' % stockModel.stock
    r = requests.get(url)
    apistock = r.json()
    valueApiStock = apistock['results'][0]['regularMarketPrice']
    dateApiStock = apistock['results'][0]['regularMarketTime']

    historyMonitoring(stock=stockModel.stock, value=valueApiStock,
                      date=dateApiStock, email=stockModel.email, monistock=stockModel).save()

    if valueApiStock >= stockModel.value_max:
        message = 'Ativo %s\n está no valor de R$%s\n Acima do valor configurado (R$ %s) para VENDA' % (
            stockModel.stock, valueApiStock, stockModel.value_max)
        send_mail(
            subject='(VENDA)Ativo %s com valor de %s!' % (
                stockModel.stock, valueApiStock),
            message=message,
            recipient_list=[stockModel.email],
            from_email=DEFAULT_FROM_EMAIL,
            fail_silently=False
        )

    if valueApiStock <= stockModel.value_min:
        message = 'Ativo %s\n está no valor de R$%s\n Abaixo do valor configurado (R$ %s) para COMPRA' % (
            stockModel.stock, valueApiStock, stockModel.value_max)
        send_mail(
            subject='(COMPRA)Ativo %s com valor de %s!' % (
                stockModel.stock, valueApiStock),
            message=message,
            recipient_list=[stockModel.email, ],
            from_email=DEFAULT_FROM_EMAIL,
            fail_silently=False
        )

    return None
