from django.urls import path, include
from .views import Index, AssignProject, login_, register, logout_, QuerysetView

urlpatterns = [
    # login and register
    path('', login_, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout_, name="logout"),
    # project page
    path('projects/', Index.as_view(), name="index"),
    path('projects/<int:pk>/', Index.as_view(), name="project_edit"),
    path('add/', Index.as_view(), name="add"),
    # employee and assign project
    path('assign/', AssignProject.as_view(), name="employees"),
    path('assign/<int:pk>/', AssignProject.as_view(), name="assign"),
    # querysets
    path('qs/', QuerysetView.as_view(), name="queryset"),
    path('qs/<int:qs_no>/', QuerysetView.as_view(), name="queryset_post"),
]
