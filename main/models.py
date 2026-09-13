from django.db import models

# Create your models here.
import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('organizaiton', 'Organization')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

    # Education
    class Education(models.Model):
        DEGREE_CHOICES = [
            ('junior-high-school', 'Middle School')
            ('high-school', 'High School'),
            ('diploma', 'Diploma'),
            ('bachelor', "Bachelor's"),
            ('master', "Master's"),
            ('doctorate', 'Doctorate'),
            ('certification', 'Certification'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, default='bachelor')
    field_of_study = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.degree} - {self.institution_name}"

    @property
    def is_ongoing(self):
        return self.ended_at is None