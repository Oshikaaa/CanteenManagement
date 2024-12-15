from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add form control attributes to the fields
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your address", "required": "required"}
        )
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your city", "required": "required"}
        )
    )

    class Meta:
        model = UserProfile
        fields = ["address", "city", "profile_picture"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class UserChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        disabled=True,  # Make email read-only
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    phone_number = forms.CharField(
        label="Phone Number",
        disabled=True,  # Make phone read-only
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    role = forms.ChoiceField(
        label="Role",
        choices=User.ROLE_CHOICE,
        disabled=True,  # Make role read-only
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["email", "phone_number", "role"]

