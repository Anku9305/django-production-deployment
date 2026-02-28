from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.student_list_view, name="student_list"),
    path("students/add/", views.student_create_view, name="student_create"),
    path(
        "students/<int:pk>/edit/",
        views.student_update_view,
        name="student_update",
    ),
    path(
        "students/<int:pk>/delete/",
        views.student_delete_view,
        name="student_delete",
    ),
    path("api/students/", views.student_list_api, name="student_list_api"),
    path(
        "api/students/<int:id>/",
        views.student_detail_api,
        name="student_detail_api",
    ),
]
