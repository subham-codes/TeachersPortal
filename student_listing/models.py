from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class StudentModel(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    subject = models.CharField(max_length=20,null=False, blank=False)
    mark = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        db_table = 'student_table'

    def __str__(self) -> str:
        return f"{self.name}"