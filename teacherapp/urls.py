from django.urls import path
from .views import *

urlpatterns = [
    path('grade/', GradeView.as_view(), name='grade'),
    path('syllabus/', SyllabusView.as_view(), name='syllabus'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('message/', MessageView.as_view(), name='message'),
    path('delete_message/<int:id>', DeleteMessageView.as_view(), name='delete_message'),
]
