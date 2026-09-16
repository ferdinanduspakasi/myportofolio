from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Experience


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
