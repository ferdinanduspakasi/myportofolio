from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "thumbnail",
            "started_at", "ended_at", "is_ongoing", "star_count",
            "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "is_ongoing"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    degree_display = serializers.CharField(source="get_degree_display", read_only=True)
    is_ongoing = serializers.ReadOnlyField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "institution_name", "degree", "degree_display",
            "field_of_study", "logo_url", "description", "started_at",
            "ended_at", "is_ongoing", "star_count", "is_starred",
        ]
        read_only_fields = ["id", "started_at", "is_ongoing"]

    def validate_institution_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institution name cannot be empty.")
        return value

    def validate_field_of_study(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Field of study cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_logo_url(self, value):
        value = strip_tags(value or "").strip()
        if value and not value.lower().startswith(("http://", "https://")):
            raise serializers.ValidationError("Logo URL must use http or https.")
        return value or None

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return any(user.pk == request.user.pk for user in obj.starred_by.all())
