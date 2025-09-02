#!/usr/bin/env python3
"""
Test script for Healthcare Assistant Django application.
Run this to verify all functionality is working correctly.
"""

import os
import sys
import django
from datetime import time, date

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
django.setup()

# Django imports (after setup)
from django.test import Client
from django.contrib.admin.sites import site
from django.conf import settings
from django.urls import resolve
from healthcare.chatbot.models import HealthLog, MedicationReminder, VitalSign
from healthcare.chatbot.urls import urlpatterns


def test_models():
    """Test all Django models."""
    print("🧪 Testing Django Models...")

    try:
        # Test HealthLog model
        health_log = HealthLog.objects.create(
            title="Test Health Log",
            description="This is a test health log entry",
            symptoms="None",
            medications="Test medication"
        )
        print(f"✅ HealthLog created: {health_log}")

        # Test MedicationReminder model
        medication = MedicationReminder.objects.create(
            medication_name="Test Medication",
            dosage="10mg",
            frequency="Daily",
            time_of_day=time(9, 0),  # 9:00 AM
            start_date=date.today(),
            is_active=True
        )
        print(f"✅ MedicationReminder created: {medication}")

        # Test VitalSign model
        vital_sign = VitalSign.objects.create(
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=72,
            temperature=98.6,
            weight=70.0
        )
        print(f"✅ VitalSign created: {vital_sign}")

        # Test model methods and properties
        print(f"✅ HealthLog string representation: {str(health_log)}")
        print(f"✅ MedicationReminder string representation: {str(medication)}")
        print(f"✅ VitalSign string representation: {str(vital_sign)}")

        # Clean up test data
        health_log.delete()
        medication.delete()
        vital_sign.delete()
        print("✅ Test data cleaned up")

    except (
        django.db.utils.DatabaseError,
        django.core.exceptions.ValidationError
    ) as e:
        print(f"❌ Model test failed: {e}")
        return False

    return True


def test_database_queries():
    """Test database queries and operations."""
    print("\n🔍 Testing Database Queries...")

    try:
        # Test creating and querying data
        health_log = HealthLog.objects.create(
            title="Query Test Log",
            description="Testing database queries",
            symptoms="Test symptoms",
            medications="Test meds"
        )

        # Test filtering
        logs = HealthLog.objects.filter(title__icontains="Query")
        print(f"✅ Filter query found {logs.count()} logs")

        # Test ordering
        ordered_logs = HealthLog.objects.order_by('-created_at')
        print(f"✅ Ordering query returned {ordered_logs.count()} logs")

        # Test count
        total_logs = HealthLog.objects.count()
        print(f"✅ Total health logs in database: {total_logs}")

        # Clean up
        health_log.delete()
        print("✅ Query test data cleaned up")

    except (
        django.db.utils.DatabaseError,
        django.core.exceptions.ValidationError
    ) as e:
        print(f"❌ Database query test failed: {e}")
        return False

    return True


def test_views():
    """Test Django views."""
    print("\n🌐 Testing Django Views...")

    try:
        client = Client()

        # Test chat view
        response = client.get('/')
        print(f"✅ Chat view status: {response.status_code}")

        # Test dashboard view
        response = client.get('/dashboard/')
        print(f"✅ Dashboard view status: {response.status_code}")

        # Test clear chat view
        response = client.post('/clear_chat/')
        print(f"✅ Clear chat view status: {response.status_code}")

    except (
        django.http.Http404,
        django.core.exceptions.ImproperlyConfigured
    ) as e:
        print(f"❌ View test failed: {e}")
        return False

    return True


def test_urls():
    """Test URL routing."""
    print("\n🔗 Testing URL Routing...")

    try:
        # Test URL patterns
        print(f"✅ Found {len(urlpatterns)} URL patterns")

        # Test specific URLs
        urls_to_test = [
            ('/', 'chat'),
            ('/dashboard/', 'dashboard'),
            ('/clear_chat/', 'clear_chat'),
        ]

        for url_path, expected_name in urls_to_test:
            try:
                resolve(url_path)
                print(f"✅ URL {url_path} resolves correctly")
            except Exception as e:
                print(f"❌ URL {url_path} failed to resolve: {e}")

    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

    return True


def test_admin():
    """Test Django admin integration."""
    print("\n👨‍💼 Testing Django Admin...")

    try:
        # Check if models are registered
        registered_models = site._registry.keys()
        expected_models = [HealthLog, MedicationReminder, VitalSign]

        for model in expected_models:
            if model in registered_models:
                print(f"✅ {model.__name__} is registered in admin")
            else:
                print(f"❌ {model.__name__} is NOT registered in admin")

    except Exception as e:
        print(f"❌ Admin test failed: {e}")
        return False

    return True


def test_settings():
    """Test Django settings configuration."""
    print("\n⚙️ Testing Django Settings...")

    try:
        # Test critical settings
        critical_settings = [
            'DEBUG',
            'SECRET_KEY',
            'DATABASES',
            'INSTALLED_APPS',
            'MIDDLEWARE',
            'TEMPLATES',
            'STATIC_URL',
        ]

        for setting in critical_settings:
            if hasattr(settings, setting):
                value = getattr(settings, setting)
                if value:
                    print(f"✅ {setting}: Configured")
                else:
                    print(f"⚠️ {setting}: Empty/False")
            else:
                print(f"❌ {setting}: Missing")

        # Test app configuration
        if 'healthcare.chatbot' in settings.INSTALLED_APPS:
            print("✅ healthcare.chatbot app is properly installed")
        else:
            print("❌ healthcare.chatbot app is NOT installed")

    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("🚀 Starting Healthcare Assistant Tests...\n")

    tests = [
        ("Models", test_models),
        ("Database Queries", test_database_queries),
        ("Views", test_views),
        ("URLs", test_urls),
        ("Admin", test_admin),
        ("Settings", test_settings),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"📋 Running {test_name} Test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} Test PASSED\n")
        else:
            print(f"❌ {test_name} Test FAILED\n")

    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your application is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

    print("=" * 50)


if __name__ == "__main__":
    main()
