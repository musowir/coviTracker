from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.shortcuts import redirect
from institutes.models import Institute, VisitedUsers
from usermanagement.models import CustomerProfile, UserFeedback
from . forms import UserForm
from django.contrib.auth import authenticate, login


class InstituitionList(generic.ListView):
    model = Institute
    template_name = "instituite/list.html"


class InstituitionVerification(generic.View):

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


class VisitedUserList(generic.ListView):
    template_name = "instituite/users_visited.html"
    ordering = ['-visited_date']
    model = VisitedUsers

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            instituition_obj = Institute.objects.get(id=id)
            queryset = VisitedUsers.objects.filter(instituite=instituition_obj).order_by('-visited_date')
        except Exception as e:
            print(e)
            queryset = []
        return queryset


class UserList(generic.ListView):
    template_name = "instituite/users_list.html"
    ordering = ['-member_since']
    model = CustomerProfile


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


class FeedbackList(generic.ListView):
    model = UserFeedback
    template_name = "instituite/users_feedback.html"
