"""
Signals for the Portfolio API application.

This module contains Django signals that can be used to perform
actions when certain events occur in the models.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact


@receiver(post_save, sender=PersonalInfo)
def clear_personal_info_cache(sender, instance, **kwargs):
    """
    Clear cache when PersonalInfo is saved.
    """
    cache.delete('personal_info_current')


@receiver(post_save, sender=Skill)
def clear_skills_cache(sender, instance, **kwargs):
    """
    Clear cache when Skill is saved.
    """
    cache.delete('skills_all')
    cache.delete(f'skills_category_{instance.category}')


@receiver(post_save, sender=Project)
def clear_projects_cache(sender, instance, **kwargs):
    """
    Clear cache when Project is saved.
    """
    cache.delete('projects_all')
    cache.delete('projects_featured')


@receiver(post_save, sender=Experience)
def clear_experience_cache(sender, instance, **kwargs):
    """
    Clear cache when Experience is saved.
    """
    cache.delete('experience_all')


@receiver(post_save, sender=Education)
def clear_education_cache(sender, instance, **kwargs):
    """
    Clear cache when Education is saved.
    """
    cache.delete('education_all')


@receiver(post_save, sender=Contact)
def clear_contact_cache(sender, instance, **kwargs):
    """
    Clear cache when Contact is saved.
    """
    cache.delete('contacts_unread_count')


@receiver(post_delete, sender=PersonalInfo)
def clear_personal_info_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when PersonalInfo is deleted.
    """
    cache.delete('personal_info_current')


@receiver(post_delete, sender=Skill)
def clear_skills_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when Skill is deleted.
    """
    cache.delete('skills_all')
    cache.delete(f'skills_category_{instance.category}')


@receiver(post_delete, sender=Project)
def clear_projects_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when Project is deleted.
    """
    cache.delete('projects_all')
    cache.delete('projects_featured')


@receiver(post_delete, sender=Experience)
def clear_experience_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when Experience is deleted.
    """
    cache.delete('experience_all')


@receiver(post_delete, sender=Education)
def clear_education_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when Education is deleted.
    """
    cache.delete('education_all')


@receiver(post_delete, sender=Contact)
def clear_contact_cache_on_delete(sender, instance, **kwargs):
    """
    Clear cache when Contact is deleted.
    """
    cache.delete('contacts_unread_count')

