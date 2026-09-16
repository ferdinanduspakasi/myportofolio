from django.urls import path

from main.views import show_main, show_experience, show_education, create_experience, get_experience_json,delete_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:project_id>/delete/",delete_experience,name="delete_experience"),
]
