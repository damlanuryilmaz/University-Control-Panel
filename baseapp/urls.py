from django.urls import path
from .views import *

urlpatterns = [
    path('main/', IndexView.as_view(), name='index'),
    path('department/', DepartmentView.as_view(), name='department'),
    path('department/<slug:slug>/', LessonView.as_view(), name='lesson'),
    path('department_request/', DepartmentRequestView.as_view(),
         name='department_request'),
    path('assign_department/', AssignDepartmentView.as_view(),
         name='assign_department'),




]
