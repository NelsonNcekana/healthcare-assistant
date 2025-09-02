import openai
from django.shortcuts import render, redirect
from django.conf import settings
from .models import HealthLog, MedicationReminder, VitalSign


def chat_view(request):
    """Main chat view for the healthcare chatbot."""
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '').strip()
        
        if user_message:
            # Initialize chat history if not exists
            if 'chat_history' not in request.session:
                request.session['chat_history'] = []
            
            # Add user message to history
            request.session['chat_history'].append({
                'role': 'user',
                'content': user_message
            })
            
            try:
                # Check if API key exists
                if not settings.OPENAI_API_KEY:
                    raise ValueError("OpenAI API key not found in settings")
                
                # Initialize OpenAI client
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                
                # Prepare messages for OpenAI
                messages = [
                    {
                        'role': 'system',
                        'content': (
                            'You are a helpful healthcare assistant. '
                            'Provide accurate, helpful health information '
                            'and guidance. Always recommend consulting '
                            'healthcare professionals for serious concerns.'
                        )
                    }
                ]
                
                # Add chat history
                for msg in request.session['chat_history']:
                    messages.append({
                        'role': msg['role'],
                        'content': msg['content']
                    })
                
                # Get AI response
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=200,
                    temperature=0.5,
                )
                
                ai_message = response.choices[0].message.content
                
                # Add AI response to history
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': ai_message
                })
                
            except openai.AuthenticationError:
                error_msg = "Authentication Error: Check your OpenAI API key"
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            except openai.RateLimitError:
                error_msg = (
                    "Rate limit exceeded. Please check your OpenAI "
                    "billing and quota."
                )
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            except openai.APITimeoutError:
                error_msg = "Request timed out. Please try again."
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            except openai.APIError as e:
                error_msg = f"OpenAI API error: {str(e)}"
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            except (ValueError, KeyError, TypeError) as e:
                error_msg = f"Configuration error: {str(e)}"
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                request.session['chat_history'].append({
                    'role': 'assistant',
                    'content': error_msg
                })
            
            # Save session
            request.session.modified = True
    
    # Get chat history for display
    chat_history = request.session.get('chat_history', [])
    
    return render(request, 'chatbot/chat.html', {
        'chat_history': chat_history
    })


def dashboard_view(request):
    """Dashboard view showing health data."""
    try:
        # Get sample data for demonstration
        health_logs = HealthLog.objects.all()[:5]
        medication_reminders = MedicationReminder.objects.filter(
            is_active=True
        )[:5]
        vital_signs = VitalSign.objects.all()[:5]
        
        context = {
            'health_logs': health_logs,
            'medication_reminders': medication_reminders,
            'vital_signs': vital_signs,
            'total_logs': HealthLog.objects.count(),
            'total_medications': MedicationReminder.objects.filter(
                is_active=True
            ).count(),
            'total_vitals': VitalSign.objects.count(),
        }
    except Exception:
        # If database tables don't exist yet, provide empty data
        context = {
            'health_logs': [],
            'medication_reminders': [],
            'vital_signs': [],
            'total_logs': 0,
            'total_medications': 0,
            'total_vitals': 0,
        }
    
    return render(request, 'chatbot/dashboard.html', context)


def clear_chat(request):
    """Clears chat history stored in the session."""
    if 'chat_history' in request.session:
        del request.session['chat_history']
    return redirect('chat')
