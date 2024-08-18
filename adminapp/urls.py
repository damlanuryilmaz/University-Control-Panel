from .views import DepartmentRequest, AssignLesson, AssignAdviser
from django.urls import path

urlpatterns = [
    path('department_and_adviser/', DepartmentRequest.as_view(),
         name='department_request'),
    path('assign_lesson/', AssignLesson.as_view(),
         name='assign_lesson'),
    path('assign_adviser/', AssignAdviser.as_view(),
         name='assign_adviser'),
]
