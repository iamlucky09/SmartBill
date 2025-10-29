from .models import User
from django import forms

class AddUserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form_title="User"

    class Meta:
        model=User
        fields='__all__'

