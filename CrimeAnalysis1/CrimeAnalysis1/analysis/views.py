from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CrimeReportForm, CrimeSearchForm, LoginForm
from .models import CrimeReport
from django.contrib.auth.decorators import login_required
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv
import json
from math import radians, cos, sin, sqrt, atan2
from django.db.models import F
from io import TextIOWrapper
from django.utils import timezone

def user_login(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # Get cleaned data from the form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication succeeds, log the user in
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to a home or dashboard page after login
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})

@login_required(login_url='/')
def user_logout(request):
    # Log the user out
    logout(request)
    
    # Add a success message
    messages.success(request, 'You have been logged out successfully.')
    
    # Redirect to the login page or home page
    return redirect('login')  # Redirect to the login page or home page after logout


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Returns distance in kilometers



@login_required(login_url='/')
def home(request):
    form = CrimeSearchForm(request.GET or None)
    crime_reports = []
    crime_by_day = []
    crime_by_month = []

    if form.is_valid():
        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        year = form.cleaned_data.get('year')
        day_of_week = form.cleaned_data.get('day_of_week')

        current_year = timezone.now().year
        # Retrieve all reports within the given year and day
        filtered_reports = CrimeReport.objects.filter(year=year, day_of_week=day_of_week)

        # Filter crimes by distance from the provided latitude/longitude
        radius = 10  # For example, search for crimes within 10 km radius
        for report in filtered_reports:
            distance = haversine(float(latitude), float(longitude), report.latitude, report.longitude)
            if distance <= radius:
                crime_reports.append({
                    'date': report.date.isoformat(),  # Format date for JavaScript
                    'crime': report.crime,
                    'latitude': report.latitude,
                    'longitude': report.longitude
                })

        # Group the crimes by day of week and month for visualization
        crime_by_day = (
            filtered_reports
            .values('day_of_week')
            .annotate(total=Count('crime'))
        )
        crime_by_month = (
            filtered_reports
            .values('month')
            .annotate(total=Count('crime'))
            .order_by('month')
        )

    return render(request, 'home.html', {
        'form': form,
        'crime_reports': crime_reports,  # Pass as a list of dictionaries
        'crime_by_day': list(crime_by_day),
        'crime_by_month': list(crime_by_month),
    })

@login_required(login_url='/')
def report_crime(request):
    form = CrimeReportForm(request.POST, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        file = form.cleaned_data['file']
        file_type = file.name.split('.')[-1].lower()  # Get file extension

        try:
            if file_type == 'csv':
                handle_csv(file)
            elif file_type == 'json':
                handle_json(file)
            elif file_type == 'xlsx':
                handle_xlsx(file)
            else:
                messages.error(request, "Unsupported file format. Please upload a CSV, JSON, or XLSX file.")
                return render(request, 'report_crime.html', {'form': form})

            messages.success(request, 'Crime data uploaded successfully!')
            return redirect('home')  # Redirect after successful submission

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

    return render(request, 'report_crime.html', {'form': form})

# Handle CSV file
def handle_csv(file):
    data = TextIOWrapper(file.file, encoding='utf-8')
    reader = csv.DictReader(data)
    for row in reader:
        CrimeReport.objects.create(
            year=int(row['year']),
            month=int(row['month']),
            date=row['date'],
            day_of_week=row['day_of_week'],
            minutes=int(row.get('minutes', 0)),
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            crime=row['crime']
        )

# Handle JSON file
def handle_json(file):
    data = json.load(file)
    for entry in data:
        CrimeReport.objects.create(
            year=entry['year'],
            month=entry['month'],
            date=entry['date'],
            day_of_week=entry['day_of_week'],
            minutes=entry.get('minutes', 0),
            latitude=entry['latitude'],
            longitude=entry['longitude'],
            crime=entry['crime']
        )

# Handle XLSX file
def handle_xlsx(file):
    df = pd.read_excel(file)  # Read the Excel file into a DataFrame
    for _, row in df.iterrows():
        CrimeReport.objects.create(
            year=int(row['year']),
            month=int(row['month']),
            date=row['date'],
            day_of_week=row['day_of_week'],
            minutes=int(row.get('minutes', 0)),
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            crime=row['crime']
        )

