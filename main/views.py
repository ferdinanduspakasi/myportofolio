from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm

# tutorial 4 authentication
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime

# otorisasi
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

# helper function for editor requirements

EDITOR_GROUP = "Editor"


def is_editor(user):
    """True jika user tergabung di Django Group 'Editor' (diatur lewat /admin)."""
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()

# return user role for role badge in navbar


def user_role(request):
    user = request.user
    if not user.is_authenticated:
        return {}
    if user.is_superuser:
        return {"user_role": "owner"}
    return {"user_role": "editor" if is_editor(user) else "user"}

# profile


def show_main(request):
    last_login = request.COOKIES.get(
        'last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# experience


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Ferdinandus Pakasi",
        "title_query": title_query,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
    experience_list = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experience_list = experience_list.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for experience in experience_list:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.get_category_display(),
                "thumbnail": experience.thumbnail,
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


# education


def show_education(request):
    # Hanya merender kerangka halaman. Data daftar dimuat browser lewat AJAX
    # dari get_education_json (lihat templates/education.html).
    context = {
        "name": "Ferdinandus Pakasi",
        "form": EducationForm(),
        "degree_choices": Education.DEGREE_CHOICES,
        "search_query": request.GET.get("q", "").strip(),
        "selected_degree": request.GET.get("degree", "").strip(),
        # Dipakai template untuk menampilkan tombol Edit bagi Editor.
        "is_editor": is_editor(request.user),
    }
    return render(request, "education.html", context)


def get_education_json(request):
    search_query = request.GET.get("q", "").strip()
    selected_degree = request.GET.get("degree", "").strip()
    education_list = Education.objects.prefetch_related("starred_by").all()

    if selected_degree:
        education_list = education_list.filter(degree=selected_degree)

    if search_query:
        education_list = education_list.filter(
            Q(institution_name__icontains=search_query)
            | Q(field_of_study__icontains=search_query)
        )

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star.
    # Hanya jumlah star dan status star milik pengguna yang sedang login yang
    # dikirim, sehingga username pengguna lain tidak terekspos di endpoint publik.
    data = []
    for education in education_list:
        # .all() memakai hasil prefetch_related, jadi tidak ada query tambahan per item.
        starred_users = list(education.starred_by.all())
        is_starred = (
            request.user.is_authenticated
            and any(u.pk == request.user.pk for u in starred_users)
        )

        data.append({
            "pk": str(education.id),
            "fields": {
                "institution_name": education.institution_name,
                "degree": education.degree,
                "degree_display": education.get_degree_display(),
                "field_of_study": education.field_of_study,
                "logo_url": education.logo_url or "",
                "description": education.description,
                "is_ongoing": education.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": is_starred,
            }
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request, "Riwayat pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
        "is_edit": False,
    }
    return render(request, "education_form.html", context)


@require_POST
def create_education_ajax(request):
    # Pengecekan peran dilakukan di sini (server), bukan hanya dengan
    # menyembunyikan tombol di template. Balasan berupa JSON, bukan redirect.
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan riwayat pendidikan."},
            status=403,
        )

    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "Riwayat pendidikan berhasil ditambahkan.",
                "pk": str(education.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_education(request, education_id):
    # Berbeda dari create/delete: Editor juga boleh mengubah data.
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


@login_required(login_url="/login/")
def toggle_education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")

# authentication


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            'last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Ferdinandus Pakasi",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response
