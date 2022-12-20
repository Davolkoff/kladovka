from django import forms


class CallRequestForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form__input", "placeholder": " "}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form__input", "placeholder": " "}))

    required_css_class = "call-request-field"

