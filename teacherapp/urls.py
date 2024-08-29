from django.urls import path
from .views import (
    GradeView,
    ContactView,
    MessageView,
    LessonSelectView,
    SubmitLessonsView,
    DeleteMessageView,
    UpdateCapacityView,
    CourseApprovalView,
    LessonSelectionView,
    UpdateWeekTableView,
)

urlpatterns = [
    path('course/<slug:slug>/', GradeView.as_view(), name='teacher_grading'),
    path('lesson-selection/', LessonSelectionView.as_view(),
         name='lesson_selection'),
    path('update_capacity/', UpdateCapacityView.as_view(),
         name='update_capacity'),
    path('update_week_table/', UpdateWeekTableView.as_view(),
         name='update_week_table'),
    path('sumbit_lessons/', SubmitLessonsView.as_view(),
         name='submit_lessons'),
    path('selected_lessons/', LessonSelectView.as_view(),
         name='selected_lessons'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('message/', MessageView.as_view(), name='message'),
    path('delete_message/<int:id>', DeleteMessageView.as_view(),
         name='delete_message'),
    path('course_approval/', CourseApprovalView.as_view(),
         name='course_approval'),
]
