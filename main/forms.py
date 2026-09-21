from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Experience, Education


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Jenis Pengalaman",
            "thumnail": "Logo institusi",
            "started_at": "Tanggal mulai",
            "ended_at": "Tanggal selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Judul pengalmanmu",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "(opsional)",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),

        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "degree",
            "field_of_study",
            "logo_url",
            "description",
            "ended_at",
        ]

        labels = {
            "institution_name": "Nama Institusi",
            "degree": "Jenjang Pendidikan",
            "field_of_study": "Bidang Studi",
            "logo_url": "URL Logo Institusi",
            "description": "Deskripsi",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Nama sekolah/universitas",
                    "maxlength": 255,
                }
            ),
            "degree": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Contoh: Ilmu Komputer",
                    "maxlength": 255,
                }
            ),
            "logo_url": URLInput(
                attrs={
                    "placeholder": "(opsional)",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman pendidikanmu",
                    "rows": 3,
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "datetime-local",
                },
            ),
        }
