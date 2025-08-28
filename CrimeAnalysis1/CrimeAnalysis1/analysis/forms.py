from django import forms
from .models import CrimeReport

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'})
    )



class CrimeReportForm(forms.Form):
    file = forms.FileField(label="Upload CSV, JSON, or XLSX")




class CrimeSearchForm(forms.Form):
    year = forms.IntegerField(required=False, label="Year")
    month = forms.ChoiceField(required=False, choices=[
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ], label="Month")
    day_of_week = forms.ChoiceField(required=False, choices=[
        ('monday', 'Monday'), ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
        ('friday', 'Friday'), ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], label="Day of the Week")
    latitude = forms.FloatField(required=False, label="Latitude")
    longitude = forms.FloatField(required=False, label="Longitude")
    # crime = forms.CharField(required=False, max_length=100, label="Crime Type")