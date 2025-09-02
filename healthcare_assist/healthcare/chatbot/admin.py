from django.contrib import admin
from .models import HealthLog, MedicationReminder, VitalSign


@admin.register(HealthLog)
class HealthLogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'symptoms')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(MedicationReminder)
class MedicationReminderAdmin(admin.ModelAdmin):
    list_display = (
        'medication_name', 'user', 'dosage', 'frequency', 
        'time_of_day', 'is_active'
    )
    list_filter = ('frequency', 'is_active', 'start_date', 'end_date')
    search_fields = ('medication_name', 'notes')
    date_hierarchy = 'start_date'
    ordering = ('time_of_day',)


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'blood_pressure_systolic', 'blood_pressure_diastolic',
        'heart_rate', 'temperature', 'weight', 'recorded_at'
    )
    list_filter = ('recorded_at',)
    search_fields = ('notes',)
    date_hierarchy = 'recorded_at'
    ordering = ('-recorded_at',)
