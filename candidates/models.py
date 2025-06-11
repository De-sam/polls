# candidates/models.py

from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    votes = models.IntegerField(default=0)  # ✅ Add this line
    # Add base64 image field
    profile_image_base64 = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.first_name} ({self.student_class}) for {self.position}"
