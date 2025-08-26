from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    """Admin configuration for PersonalInfo model."""
    
    list_display = ('name', 'title', 'email', 'location', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'title', 'email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'website'),
            'classes': ('collapse',)
        }),
        ('Files', {
            'fields': ('profile_image', 'resume'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        """Only allow one PersonalInfo instance."""
        return not PersonalInfo.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model."""
    
    list_display = ('name', 'category', 'proficiency', 'order', 'get_proficiency_bar')
    list_filter = ('category', 'proficiency')
    search_fields = ('name', 'description')
    ordering = ('category', 'order', 'name')
    list_editable = ('order', 'proficiency')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'icon')
        }),
        ('Proficiency & Order', {
            'fields': ('proficiency', 'order')
        })
    )
    
    def get_proficiency_bar(self, obj):
        """Display proficiency as a visual bar."""
        filled = '█' * obj.proficiency
        empty = '░' * (10 - obj.proficiency)
        return format_html(
            '<span style="font-family: monospace; color: #007cba;">{}</span>'
            '<span style="font-family: monospace; color: #ddd;">{}</span> {}',
            filled, empty, obj.proficiency
        )
    get_proficiency_bar.short_description = 'Proficiency'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""
    
    list_display = ('title', 'featured', 'order', 'get_technologies', 'created_at')
    list_filter = ('featured', 'technologies', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    filter_horizontal = ('technologies',)
    ordering = ('-featured', 'order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('featured', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'description')
        }),
        ('Media & Links', {
            'fields': ('image', 'github_url', 'live_url')
        }),
        ('Settings', {
            'fields': ('technologies', 'featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_technologies(self, obj):
        """Display technologies as a comma-separated list."""
        return ', '.join([tech.name for tech in obj.technologies.all()[:3]])
    get_technologies.short_description = 'Technologies'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin configuration for Experience model."""
    
    list_display = ('position', 'company', 'location', 'start_date', 'end_date', 'current', 'order')
    list_filter = ('current', 'start_date', 'company')
    search_fields = ('position', 'company', 'description', 'achievements')
    filter_horizontal = ('technologies_used',)
    ordering = ('-start_date', 'order')
    list_editable = ('order', 'current')
    
    fieldsets = (
        ('Position Details', {
            'fields': ('position', 'company', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'current')
        }),
        ('Content', {
            'fields': ('description', 'achievements')
        }),
        ('Technologies & Order', {
            'fields': ('technologies_used', 'order')
        })
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Admin configuration for Education model."""
    
    list_display = ('degree', 'field_of_study', 'institution', 'start_date', 'end_date', 'current', 'gpa', 'order')
    list_filter = ('current', 'start_date', 'institution')
    search_fields = ('degree', 'field_of_study', 'institution', 'description')
    ordering = ('-start_date', 'order')
    list_editable = ('order', 'current')
    
    fieldsets = (
        ('Institution Details', {
            'fields': ('institution', 'degree', 'field_of_study')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'current')
        }),
        ('Academic Information', {
            'fields': ('description', 'gpa', 'achievements')
        }),
        ('Display Order', {
            'fields': ('order',)
        })
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model."""
    
    list_display = ('name', 'email', 'subject', 'created_at', 'read', 'get_message_preview')
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('read',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('read', 'created_at')
        })
    )
    
    def get_message_preview(self, obj):
        """Display a preview of the message."""
        preview = obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return preview
    get_message_preview.short_description = 'Message Preview'
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read."""
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        """Mark selected messages as unread."""
        updated = queryset.update(read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"
