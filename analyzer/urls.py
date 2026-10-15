from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('analysis/new/', views.new_analysis, name='new_analysis'),
    path('analysis/<int:pk>/', views.result, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('jobs/add/', views.add_job, name='add_job'),
    path('jobs/<int:pk>/toggle/', views.toggle_job, name='toggle_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('analysis/job/<int:job_id>/', views.analyze_job, name='analyze_job'),
    path('analysis/<int:pk>/delete/', views.delete_analysis, name='delete_analysis'),
    path('jobs/<int:pk>/results/', views.job_results, name='job_results'),
]
