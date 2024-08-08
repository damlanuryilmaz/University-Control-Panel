from django.urls import path
from .views import *

urlpatterns = [
    path('main/', IndexView.as_view(), name='index'),
    path('department/', DepartmentView.as_view(), name='department'),
    path('department/<slug:slug>/', LessonView.as_view(), name='lesson'),
    path('lesson_list/<int:id>', NavbarView.as_view(), name='lesson_list'),



]
