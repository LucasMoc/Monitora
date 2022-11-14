
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from .services import getListCompany, strockMonitoringService
from .models import monitoringStock, historyMonitoring
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from background_task.models import Task


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        listCompanys = getListCompany()
        search = self.request.GET.get('search')
        if search:
            searchComapnys = list(
                filter(lambda x: x['stock'] == search or x['name'] == search, listCompanys))
            context['listaAtivos'] = searchComapnys
        else:
            context['listaAtivos'] = listCompanys
        return context


class registerMonitForms(CreateView):
    model = monitoringStock
    template_name = 'registerMonitoring.html'
    fields = ['stock', 'value_max', 'value_min', 'moniTime', 'email']
    success_url = reverse_lazy('myStock')

    def form_valid(self, form):
        stock = form.cleaned_data['stock']
        moniTime_sec = form.cleaned_data['moniTime']*60*60
        strockMonitoringService(stock, repeat=moniTime_sec,
                                repeat_until=None, verbose_name='%s' % stock)
        return super().form_valid(form)


class registerWithStockMonitForms(CreateView):
    model = monitoringStock
    template_name = 'registerMonitoring.html'
    fields = ['stock', 'value_max', 'value_min', 'moniTime', 'email']
    success_url = reverse_lazy('myStock')

    def get_initial(self):
        stock = self.kwargs.get("stock")
        return {'stock': stock}

    def form_valid(self, form):
        stock = form.cleaned_data['stock']
        moniTime_sec = form.cleaned_data['moniTime']*60
        strockMonitoringService(stock, repeat=moniTime_sec,
                                repeat_until=None, verbose_name='%s' % stock)
        return super().form_valid(form)


class EditMonitForms(UpdateView):
    model = monitoringStock
    template_name = 'registerMonitoring.html'
    fields = ['stock', 'value_max', 'value_min', 'moniTime', 'email']
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('myStock')

    def form_valid(self, form):
        form.save()
        pk_ = self.kwargs.get("pk")
        stock = monitoringStock.objects.get(pk=pk_)

        Task.objects.get(verbose_name=stock.stock).delete()

        stockName = form.cleaned_data['stock']
        moniTime_sec = form.cleaned_data['moniTime']*60*60
        strockMonitoringService(
            stockName, repeat=moniTime_sec, repeat_until=None, verbose_name='%s' % stockName)
        return super().form_valid(form)


class DeleteMonitForms(DeleteView):
    model = monitoringStock
    template_name = 'deleteMonitoring.html'
    success_url = reverse_lazy('myStock')

    def form_valid(self, form):
        pk_ = self.kwargs.get("pk")
        stock = monitoringStock.objects.get(pk=pk_)
        Task.objects.get(verbose_name=stock.stock).delete()
        return super().form_valid(form)


class myStock(ListView):
    models = monitoringStock
    template_name = 'myStock.html'
    queryset = monitoringStock.objects.all()
    context_object_name = 'listStocks'


class historyMonitoringView(ListView):
    models = monitoringStock
    template_name = 'histStock.html'
    queryset = historyMonitoring.objects.all()
    context_object_name = 'histStocks'
