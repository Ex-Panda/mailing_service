from django import forms

from mailing.models import Mailing, Client


class NiceForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(NiceForm, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'time_mailing', 'period', 'matter_letter', 'message_body', 'client',)

    def __init__(self, user, *args, **kwargs):
        #функция возвращает пользователю только его клиентов при создании формы рассылки
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=user)


class ClientForm(NiceForm, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'name', 'comment',)
