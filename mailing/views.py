from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article
from customer.models import Customer
from mailing.forms import CreateMailingForm, UpdateMailingForm
from mailing.models import Mailing, Log


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        queryset = Mailing.objects.filter(user=self.request.user, is_active=True)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'log_list_{self.object.pk}'
            log_list = cache.get(key)
            if log_list is None:
                log_list = Log.objects.filter(mailing__pk=self.object.pk)
                cache.set(key, log_list)
        else:
            log_list = Log.objects.filter(mailing__pk=self.object.pk)
        context_data['logs'] = log_list

        return context_data


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} {email} {message}')
    context = {
        'title': "Контакты"
    }
    return render(request, 'mailing/contact.html', context)


def main(request):
    customers = len(Customer.objects.all().distinct('email'))
    article = Article.objects.filter(is_published=True).order_by('?')
    mailing = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(status='started'))
    context = {
        'title': "Главная",
        'article': article[:3],
        'mailing': mailing,
        'mailing_active': mailing_active,
        'customers': customers
    }
    return render(request, 'mailing/main.html', context)


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    permission_required = 'mailing.add_mailing'
    form_class = CreateMailingForm
    success_url = reverse_lazy('mailing:list')

    def get(self, request, **kwargs):
        form = self.form_class(self.request.user, request.POST)
        context = {
            'form': form,
        }
        customers = Customer.objects.filter(user=self.request.user)
        context['customers'] = customers
        return render(request, 'mailing/mailing_form.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            customers = form.cleaned_data.get('customers')
            if not customers:
                form.add_error('customers', 'Выберите хотя бы одного клиента.')
            mailing = form.save(commit=False)
            mailing.user = self.request.user
            mailing.is_active = True
            mailing.save()
            form.save_m2m()
            return redirect(self.success_url)

        else:
            return render(request, 'mailing/no_customer.html')


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = UpdateMailingForm
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.filter(user=self.request.user)
        context['customers'] = customers
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:list')


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'mailing/log_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DetailLogView(LoginRequiredMixin, DetailView):
    model = Log
    template_name = 'mailing/log_detail.html'


class DeleteLogView(LoginRequiredMixin, DeleteView):
    model = Log
    template_name = 'mailing/log_confirm_delete.html'
    success_url = reverse_lazy('mailing:log_list')


@permission_required('mailing.set_active')
def toggle_activity(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True

    mailing_item.save()

    return redirect(reverse('mailing:list'))
