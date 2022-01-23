from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.shortcuts import redirect
from institutes.models import Institute, VisitedUsers, AlertLog
from usermanagement.models import CustomerProfile, UserFeedback,UserPositivityLog
from . forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from functools import reduce
import operator
from django.contrib.auth.mixins import LoginRequiredMixin


class InstituitionList(LoginRequiredMixin, generic.ListView):
    model = Institute
    template_name = "instituite/list.html"
    login_url = '/login/'


class InstituitionVerification(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    def get(self, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            instituition_obj = Institute.objects.get(id=id)
        except Exception as e:
            print(e)
            messages.success(self.request, "Invalid Instituition Id.")
        else:
            instituition_obj.is_verified = True
            instituition_obj.save()
            messages.success(self.request, "Instituition verified successfully.")
        return redirect(reverse_lazy('InstituitionList'))


class VisitedUserList(LoginRequiredMixin, generic.ListView):
    template_name = "instituite/users_visited.html"
    ordering = ['-visited_date']
    model = VisitedUsers
    login_url = '/login/'

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            instituition_obj = Institute.objects.get(id=id)
            queryset = VisitedUsers.objects.filter(instituite=instituition_obj).order_by('-visited_date')
        except Exception as e:
            print(e)
            queryset = []
        return queryset


class UserList(LoginRequiredMixin, generic.ListView):
    template_name = "instituite/users_list.html"
    ordering = ['-member_since']
    model = CustomerProfile
    login_url = '/login/'

    def get_queryset(self, *args, **kwargs):
        print(self.request.GET)
        q = self.request.GET.get('q')
        if q:
            filter_list = (Q(phone_number=q)|Q(user__email=q)|Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q))
            queryset = self.model.objects.filter(filter_list)
        else:
            queryset = self.model.objects.all()
        return queryset


class PositiveUserList(LoginRequiredMixin, generic.ListView):
    template_name = "instituite/positive_list.html"
    ordering = ['-member_since']
    model = CustomerProfile
    login_url = '/login/'

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(covid_status='P')
        return queryset


class UserCovidHistoryList(LoginRequiredMixin, generic.DetailView):
    model = CustomerProfile
    template_name = "instituite/covid_history.html"
    login_url = '/login/'

class ChangeCovidStatus(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    model = CustomerProfile

    def post(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        try:
            user_ob = self.model.objects.get(id=id)
            if user_ob.covid_status == 'N':
                user_ob.covid_status = 'P'
            else:
                user_ob.covid_status = 'N'
            UserPositivityLog.objects.create(customer=user_ob, covid_status=user_ob.covid_status)
            user_ob.save()
            msg = "Successfully updated the covid status of " + user_ob.get_full_name().title()
            messages.success(self.request, msg)
            return redirect(self.request.META.get('HTTP_REFERER'))
        except Exception as e:
            print(e)
            messages.error(self.request, "Invalid User ID!.")
            return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(self.request.META.get('HTTP_REFERER'))


class Login(generic.FormView):
    form_class = UserForm
    success_url = reverse_lazy('Login')
    template_name = "instituite/register.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user_ob = form.get_profile_object()
        print(user_ob)
        if not user_ob: 
            messages.error(self.request, "Invalid login credentials!")
            return redirect(self.request.META.get('HTTP_REFERER'))
        password = form.cleaned_data['password']
        print("pass", password, user_ob.username)
        user = authenticate(username=user_ob.username, password=password)
        print("userrr", user)
        # send OTP
        if user:
            self.object = user_ob
            login(self.request, user)
            if self.object.is_staff:
                return redirect(reverse_lazy('UserList'))
            else:
                messages.error(self.request, "Invalid login credentials!")
                return redirect(self.request.META.get('HTTP_REFERER'))      

        else:
            messages.error(self.request, "Invalid login credentials!")
        return redirect(self.request.META.get('HTTP_REFERER'))


class FeedbackList(LoginRequiredMixin, generic.ListView):
    model = UserFeedback
    template_name = "instituite/users_feedback.html"
    login_url = '/login/'


class Logout(generic.View):

    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse_lazy('Login'))


class AlertList(generic.ListView):
    model = AlertLog
    template_name = "instituite/alert_list.html"
    login_url = '/login/'

