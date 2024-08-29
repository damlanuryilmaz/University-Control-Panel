from django.urls import path
from .views import (
    IndexView,
    LessonView,
    DepartmentView,
    UploadPhotoView,
    DepartmentRequestView,
)

urlpatterns = [
    path('main/', IndexView.as_view(), name='index'),
    path('department/', DepartmentView.as_view(), name='department'),
    path('department/<slug:slug>/', LessonView.as_view(), name='lesson'),
    path('student_request/', DepartmentRequestView.as_view(),
         name='student_request'),
    path('upload_photo/', UploadPhotoView.as_view(), name='upload_photo'),
]
