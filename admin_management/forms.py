import operator
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from functools import reduce
from django.core.exceptions import ObjectDoesNotExist




class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=dict(max_length=25, 
                                                                placeholder='Username')),
                            error_messages={'required': 'Username is required!.'})
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(
                                                                    required=True, 
                                                                    max_length=30, 
                                                                    render_value=False, 
                                                                    placeholder='Password'),
                                                          ),
                                                          label=("Password"), 
                            error_messages={'required': 'Password is required!'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            self.user_ob = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Invalid Username')
        return username
    
    def get_profile_object(self):
        return self.user_ob
        
    class Meta:
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        self.user_ob = None
        super(UserForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = "form-control form-control-lg"