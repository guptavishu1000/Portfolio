from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from django.templatetags.static import static
from . import views

router = DefaultRouter()
router.register(r'personal-info', views.PersonalInfoViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'education', views.EducationViewSet)
router.register(r'contact', views.ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 