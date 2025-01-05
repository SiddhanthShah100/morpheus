from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_form, name='create_form'),
    path('view/', views.view_forms, name='view_forms'),
     path('<int:form_id>/submit/', views.submit_response, name='submit_response'),
    path('<int:form_id>/respond/', views.respond_to_form, name='respond_to_form'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('<int:form_id>/responses/', views.view_responses, name='view_responses'),
    path('<int:form_id>/analytics/', views.view_analytics, name='view_analytics'),
    path('submit_response/<int:form_id>/', views.submit_response, name='submit_response'),
]
