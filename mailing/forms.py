from django import forms

from customer.models import Customer
from mailing.models import Mailing


class CreateMailingForm(forms.ModelForm):
    mailing_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        ),
        label='Дата и время рассылки'
    )

    customers = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Клиенты'
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст'}),
        label='Тема сообщения'
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Введите текст'}),
        label='Текст сообщения'
    )

    class Meta:
        model = Mailing
        exclude = ('status', 'user', 'is_active')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = Customer.objects.filter(user=user)


class UpdateMailingForm(forms.ModelForm):

    mailing_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        ),
        label='Дата и время рассылки'
    )

    customers = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Клиенты'
    )

    class Meta:
        model = Mailing
        fields = ('mailing_time', 'periodicity', 'customers')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = Customer.objects.filter(user=user)
