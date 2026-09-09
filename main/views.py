from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Ferdinandus Pakasi",
        "npm": "2506602643",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Computer Science student with a strong passion" 
            "for technology, science, and innovation. Enthusiastic" 
            "about exploring the intersection of science and" 
            "technology, particularly how the digital world can drive" 
            "meaningful solutions for society."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Ferdinandus Pakasi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)