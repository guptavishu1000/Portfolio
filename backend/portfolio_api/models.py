from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from .constants import (
    SKILL_CATEGORIES, PROFICIENCY_CHOICES, GPA_MIN, GPA_MAX,
    UPLOAD_PATHS, VALIDATION_MESSAGES
)


class PersonalInfo(models.Model):
    """
    Model to store personal information for the portfolio owner.
    Only one instance should exist at a time.
    """
    name = models.CharField(max_length=100, help_text="Full name")
    title = models.CharField(max_length=200, help_text="Professional title or role")
    bio = models.TextField(help_text="Professional biography or summary")
    email = models.EmailField(help_text="Primary email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number (optional)")
    location = models.CharField(max_length=100, blank=True, help_text="City, Country (optional)")

    # Social links
    github = models.URLField(blank=True, help_text="GitHub profile URL (optional)")
    linkedin = models.URLField(blank=True, help_text="LinkedIn profile URL (optional)")
    twitter = models.URLField(blank=True, help_text="Twitter profile URL (optional)")
    website = models.URLField(blank=True, help_text="Personal website URL (optional)")

    # Instead of ImageField/FileField use CharField to store static paths:
    profile_image = models.CharField(
        max_length=200, 
        default="assets/images/profile_pic.png",
        help_text="Path in static files"
    )
    resume = models.CharField(
        max_length=200,
        default="assets/docs/resume.pdf",
        help_text="Path in static files"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def profile_image_url(self):
        from django.templatetags.static import static
        return static(self.profile_image)

    def resume_url(self):
        from django.templatetags.static import static
        return static(self.resume)


    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} - {self.title}"

    def save(self, *args, **kwargs):
        """Ensure only one PersonalInfo instance exists"""
        if not self.pk and PersonalInfo.objects.exists():
            raise ValueError(VALIDATION_MESSAGES['only_one_personal_info'])
        super().save(*args, **kwargs)


class Skill(models.Model):
    """Model to store technical and soft skills with proficiency levels."""
    
    name = models.CharField(max_length=100, help_text="Skill name")
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, help_text="Skill category")
    proficiency = models.IntegerField(
        choices=PROFICIENCY_CHOICES,
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Proficiency level from 1-10"
    )
    description = models.TextField(blank=True, help_text="Skill description (optional)")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class (FontAwesome, etc.)")
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")
    
    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    """Model to store portfolio projects with technologies and links."""
    
    title = models.CharField(max_length=200, help_text="Project title")
    description = models.TextField(help_text="Detailed project description")
    short_description = models.CharField(max_length=300, help_text="Brief project summary")
    image = models.ImageField(upload_to=UPLOAD_PATHS['projects'], blank=True, help_text="Project screenshot (optional)")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL (optional)")
    live_url = models.URLField(blank=True, help_text="Live demo URL (optional)")
    technologies = models.ManyToManyField(Skill, related_name='projects', help_text="Technologies used")
    featured = models.BooleanField(default=False, help_text="Mark as featured project")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-featured', 'order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title


class Experience(models.Model):
    """Model to store work experience with achievements and technologies."""
    
    company = models.CharField(max_length=200, help_text="Company name")
    position = models.CharField(max_length=200, help_text="Job title/position")
    location = models.CharField(max_length=100, blank=True, help_text="Work location (optional)")
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(null=True, blank=True, help_text="End date (leave blank if current)")
    current = models.BooleanField(default=False, help_text="Currently working here")
    description = models.TextField(help_text="Job description and responsibilities")
    achievements = models.TextField(blank=True, help_text="Key achievements and accomplishments")
    technologies_used = models.ManyToManyField(
        Skill, 
        related_name='experiences', 
        blank=True,
        help_text="Technologies used in this role"
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experience"
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    def clean(self):
        """Validate that end_date is after start_date and current is set appropriately."""
        from django.core.exceptions import ValidationError
        
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(VALIDATION_MESSAGES['end_date_before_start'])
        
        if self.current and self.end_date:
            raise ValidationError(VALIDATION_MESSAGES['current_with_end_date'])


class Education(models.Model):
    """Model to store educational background and achievements."""
    
    institution = models.CharField(max_length=200, help_text="Educational institution name")
    degree = models.CharField(max_length=200, help_text="Degree obtained")
    field_of_study = models.CharField(max_length=200, help_text="Field of study/major")
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(null=True, blank=True, help_text="End date (leave blank if current)")
    current = models.BooleanField(default=False, help_text="Currently studying here")
    description = models.TextField(blank=True, help_text="Additional details about the program")
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(GPA_MIN), MaxValueValidator(GPA_MAX)],
        help_text="GPA (0.00-4.00 scale, optional)"
    )
    achievements = models.TextField(blank=True, help_text="Academic achievements and honors")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"
    
    def clean(self):
        """Validate that end_date is after start_date and current is set appropriately."""
        from django.core.exceptions import ValidationError
        
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(VALIDATION_MESSAGES['end_date_before_start'])
        
        if self.current and self.end_date:
            raise ValidationError(VALIDATION_MESSAGES['current_with_end_date'])


class Contact(models.Model):
    """Model to store contact form submissions from visitors."""
    
    name = models.CharField(max_length=100, help_text="Visitor's name")
    email = models.EmailField(help_text="Visitor's email address")
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message content")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, help_text="Mark as read")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
