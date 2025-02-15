from django.db import models

class User(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Ensure this field is defined
    level = models.TextField(blank=True, null=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fullname}"

class LearningEnglish(models.Model):
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Elementary", "Elementary"),
        ("Pre-Intermediate", "Pre-Intermediate"),
        ("Intermediate", "Intermediate"),
        ("IELTS", "IELTS"),
    ]

    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, unique=True)
    listening = models.FileField(upload_to='listening/', blank=True, null=True)
    reading = models.FileField(upload_to='reading/', blank=True, null=True)
    writing = models.FileField(upload_to='writing/', blank=True, null=True)
    speaking = models.FileField(upload_to='speaking/', blank=True, null=True)

    def __str__(self):
        return self.level