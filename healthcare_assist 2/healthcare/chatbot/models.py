from django.db import models
from django.contrib.auth.models import User


class HealthLog(models.Model):
    """Model for storing health logs."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    symptoms = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"


class MedicationReminder(models.Model):
    """Model for medication reminders."""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times', 'Three Times Daily'),
        ('weekly', 'Weekly'),
        ('as_needed', 'As Needed'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    time_of_day = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_of_day']

    def __str__(self):
        return f"{self.medication_name} - {self.frequency}"


class VitalSign(models.Model):
    """Model for storing vital signs."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Vitals - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
