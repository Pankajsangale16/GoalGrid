from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Client, Task


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me') == 'on'
        
        if email and password:
            # Django uses username, but we'll allow email login
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                # Try username if email doesn't work
                username = email
                user = None
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email/username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'tasks/login.html')


def register_view(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        elif password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'tasks/register.html')


def forgot_password_view(request):
    """
    Simple in-page password reset:
    - No email
    - User enters email/username + new password + confirm password
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = []

        if not identifier:
            errors.append('Please enter your email or username.')

        if not new_password or not confirm_password:
            errors.append('Please enter and confirm your new password.')
        elif len(new_password) < 8:
            errors.append('New password must be at least 8 characters long.')
        elif new_password != confirm_password:
            errors.append('New password and confirm password do not match.')

        user = None
        if not errors:
            # Try find by email first, then by username
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=identifier)
                except User.DoesNotExist:
                    errors.append('User not found with that email or username.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully. Please log in with your new password.')
            return redirect('login')

    return render(request, 'tasks/forgot_password.html')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard showing all clients with their tasks"""
    # Only show current user's clients
    clients = Client.objects.prefetch_related('tasks').filter(user=request.user)
    
    # Calculate global dashboard progress (only for current user)
    all_tasks = Task.objects.filter(client__user=request.user)
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(is_completed=True).count()
    
    if total_tasks > 0:
        global_completion = round((completed_tasks / total_tasks) * 100)
        global_remaining = 100 - global_completion
    else:
        global_completion = 0
        global_remaining = 0
    
    context = {
        'clients': clients,
        'total_clients': clients.count(),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': total_tasks - completed_tasks,
        'global_completion': global_completion,
        'global_remaining': global_remaining,
    }
    return render(request, 'tasks/dashboard.html', context)


@require_POST
@login_required
def client_create(request):
    """Create a new client"""
    client_name = request.POST.get('name', '').strip()
    
    if not client_name:
        return JsonResponse({'success': False, 'error': 'Client name is required'}, status=400)
    
    # Check if client exists for this user only
    if Client.objects.filter(user=request.user, name=client_name).exists():
        return JsonResponse({'success': False, 'error': 'Client with this name already exists'}, status=400)
    
    client = Client.objects.create(user=request.user, name=client_name)
    
    return JsonResponse({
        'success': True,
        'client': {
            'id': client.id,
            'name': client.name,
            'completion_percentage': client.completion_percentage,
            'remaining_percentage': client.remaining_percentage,
            'total_tasks': client.total_tasks,
            'completed_tasks': client.completed_tasks,
        }
    })


@require_POST
@login_required
def client_delete(request, pk):
    """Delete a client and all its tasks"""
    # Only allow deleting own clients
    client = get_object_or_404(Client, pk=pk, user=request.user)
    client_name = client.name
    client.delete()
    messages.success(request, f'Client "{client_name}" and all its tasks deleted successfully!')
    return redirect('dashboard')


@require_POST
@login_required
def task_create(request, client_id):
    """Create a new task for a client"""
    # Only allow creating tasks for own clients
    client = get_object_or_404(Client, pk=client_id, user=request.user)
    task_title = request.POST.get('title', '').strip()
    
    if not task_title:
        return JsonResponse({'success': False, 'error': 'Task title is required'}, status=400)
    
    task = Task.objects.create(client=client, title=task_title)
    
    # Recalculate client progress
    client.refresh_from_db()
    
    return JsonResponse({
        'success': True,
        'task': {
            'id': task.id,
            'title': task.title,
            'is_completed': task.is_completed,
        },
        'client': {
            'completion_percentage': client.completion_percentage,
            'remaining_percentage': client.remaining_percentage,
            'total_tasks': client.total_tasks,
            'completed_tasks': client.completed_tasks,
        }
    })


@require_POST
@login_required
def task_toggle(request, pk):
    """Toggle task completion status via AJAX"""
    # Only allow toggling own tasks
    task = get_object_or_404(Task, pk=pk, client__user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    
    # Recalculate client progress
    client = task.client
    client.refresh_from_db()
    
    # Recalculate global progress (only for current user)
    all_tasks = Task.objects.filter(client__user=request.user)
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(is_completed=True).count()
    
    if total_tasks > 0:
        global_completion = round((completed_tasks / total_tasks) * 100)
        global_remaining = 100 - global_completion
    else:
        global_completion = 0
        global_remaining = 0
    
    return JsonResponse({
        'success': True,
        'is_completed': task.is_completed,
        'client': {
            'id': client.id,
            'completion_percentage': client.completion_percentage,
            'remaining_percentage': client.remaining_percentage,
            'total_tasks': client.total_tasks,
            'completed_tasks': client.completed_tasks,
        },
        'global': {
            'completion_percentage': global_completion,
            'remaining_percentage': global_remaining,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
        }
    })


@require_POST
@login_required
def task_delete(request, pk):
    """Delete a task"""
    # Only allow deleting own tasks
    task = get_object_or_404(Task, pk=pk, client__user=request.user)
    client = task.client
    task.delete()
    
    # Recalculate client progress
    client.refresh_from_db()
    
    return JsonResponse({
        'success': True,
        'client': {
            'id': client.id,
            'completion_percentage': client.completion_percentage,
            'remaining_percentage': client.remaining_percentage,
            'total_tasks': client.total_tasks,
            'completed_tasks': client.completed_tasks,
        }
    })
