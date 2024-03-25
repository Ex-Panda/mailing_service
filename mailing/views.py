from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm
from mailing.models import Mailing, MailingLog, Client


class ProtectedView(View):
    #переопределение get, чтобы анонимный пользователь не мог взаимодействовать
    def get(self, *args, **kwargs):
        if self.request.user.id is None:
            return redirect('user_auth:login')
        else:
            return super().get(*args, **kwargs)


class ChecksUser:
    def get_object(self, queryset=None):
        #переопределяю метод, получаю объект, проверяю пользователя по требованиям
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingCreateView(ProtectedView, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        #создатель закрепляется за рассылкой
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.owner = self.request.user
            new_mailing.date_next_mailing = new_mailing.start_time
            new_mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        #добавляем юзера в словарь аргументов
        user_request = super().get_form_kwargs()
        user_request['user'] = self.request.user
        return user_request


class MailingListView(ProtectedView, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        #менеджер видит все рассылки
        if self.request.user.has_perm('mailing.mailing_published') or self.request.user.is_superuser:
            mailing = super().get_queryset()
            return mailing
        #пользователь видит только свои рассылки
        else:
            mailing = super().get_queryset()
            return mailing.filter(owner=self.request.user)


class MailingDetailView(ProtectedView, ChecksUser, DetailView):
    model = Mailing
    template_name = 'mailing/mailing.html'

    def get_object(self, queryset=None):
        #переопределяю метод, получаю объект, проверяю пользователя по требованиям
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser and not self.request.user.has_perm('mailing.mailing_published'):
            raise Http404
        return self.object


class MailingUpdateView(ProtectedView, ChecksUser, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        #добавляем юзера в словарь аргументов
        user_request = super().get_form_kwargs()
        user_request['user'] = self.request.user
        return user_request


class MailingDeleteView(ProtectedView, ChecksUser, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingLogListView(ProtectedView, ListView):
    model = MailingLog
    template_name = 'mailing/logs_mailing.html'

    def get_queryset(self):
        logs = super().get_queryset()
        pk_mailing = self.kwargs['pk']
        return logs.filter(mailing_id=pk_mailing, mailing__owner=self.request.user)


class ClientCreateView(ProtectedView, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        #создатель закрепляется за рассылкой
        if form.is_valid():
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()
        return super().form_valid(form)


class ClientListView(ProtectedView, ListView):
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        client = super().get_queryset()
        return client.filter(owner=self.request.user)


class ClientDetailView(ProtectedView, ChecksUser, DetailView):
    model = Client
    template_name = 'mailing/client.html'


class ClientUpdateView(ProtectedView, ChecksUser, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(ProtectedView, ChecksUser, DeleteView):
    model = Client
    template_name = 'mailing/client_delete.html'
    success_url = reverse_lazy('mailing:client_list')


class MailingBlock(View):

    def get(self, request, *args, **kwargs):
        mailing_id = kwargs.get('id')
        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = 'blocked'
        mailing.save()
        return redirect('mailing:mailing_list')


class HomeTemplateView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Mailing.objects.all().count()
        context['mailing_active'] = Mailing.objects.filter(status='started').count()
        context['client_unique'] = Client.objects.all().count()
        context['blog'] = Blog.objects.all().order_by("?")[:3]
        return context
