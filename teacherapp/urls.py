from django.urls import path
from .views import (
    GradeView,
    ContactView,
    MessageView,
    DeleteMessageView,
    LessonSelectionView,
)

urlpatterns = [
    path('grade/', GradeView.as_view(), name='grade'),
    path('lesson-selection/', LessonSelectionView.as_view(),
         name='lesson_selection'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('message/', MessageView.as_view(), name='message'),
    path('delete_message/<int:id>', DeleteMessageView.as_view(),
         name='delete_message'),
]
