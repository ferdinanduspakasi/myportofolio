from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm

# profile


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

# experience


def show_experience(request):
    json_response = get_experience_json(request)

    experience = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience = [e.object for e in experience]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Ferdinandus Pakasi",
        "experience_list": experience,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = Experience.objects.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience)
    return HttpResponse(experience_json, content_type="application/json")


def delete_experience(request, project_id):
    experience = get_object_or_404(Experience, pk=project_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# education


def show_education(request):
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [e.object for e in education]
    selected_degree = request.GET.get("degree", "")

    context = {
        "name": "Ferdinandus Pakasi",
        "education_list": education_list,
        "degree_choices": Education.DEGREE_CHOICES,
        "selected_degree": selected_degree,
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
        "is_edit": False,
    }
    return render(request, "education_form.html", context)


def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
        "is_edit": True,
        "education": education,
    }
    return render(request, "education_form.html", context)


def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


def get_education_json(request):
    selected_degree = request.GET.get("degree", "").strip()
    education = Education.objects.all()

    if selected_degree:
        education = education.filter(degree=selected_degree)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")