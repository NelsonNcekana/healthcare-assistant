from django.core.management.base import BaseCommand
from healthcare.chatbot.models import HealthLog, MedicationReminder, VitalSign
from datetime import date, time


class Command(BaseCommand):
    help = 'Create sample health data for demonstration'

    def handle(self, *args, **options):
        # Create sample health log
        health_log, created = HealthLog.objects.get_or_create(
            title="Daily Health Check",
            defaults={
                'description': 'Feeling good today, no symptoms to report.',
                'symptoms': 'None',
                'medications': 'Daily vitamins'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created sample health log')
            )

        # Create sample medication reminder
        medication, created = MedicationReminder.objects.get_or_create(
            medication_name="Daily Vitamins",
            defaults={
                'dosage': '1 tablet',
                'frequency': 'daily',
                'time_of_day': time(9, 0),  # 9:00 AM
                'start_date': date.today(),
                'is_active': True,
                'notes': 'Take with breakfast'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created sample medication reminder')
            )

        # Create sample vital signs
        vital_sign, created = VitalSign.objects.get_or_create(
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            defaults={
                'heart_rate': 72,
                'temperature': 98.6,
                'weight': 70.0,
                'notes': 'Normal readings'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created sample vital signs')
            )

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )
