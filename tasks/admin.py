from django.contrib import admin
from .models import Client, Task


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total_tasks', 'completed_tasks', 'completion_percentage', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'client_user', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'client', 'created_at']
    search_fields = ['title', 'client__name', 'client__user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def client_user(self, obj):
        return obj.client.user.username
    client_user.short_description = 'User'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(client__user=request.user)

