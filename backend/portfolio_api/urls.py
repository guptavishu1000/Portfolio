from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from django.views.generic.base import RedirectView
from django.templatetags.static import static
from . import views

class SingletonRouter(SimpleRouter):
    """
    A router for singleton resources.
    The API looks something like this:
    /personal-info/ - GET: retrieve, PUT: update, PATCH: partial_update
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # For listing (GET without ID) - we'll handle this in the view
        Route(
            url=r'^{prefix}/list{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
    ]

router = DefaultRouter()
# Register the singleton view
singleton_router = SingletonRouter()
singleton_router.register(r'personal-info', views.PersonalInfoViewSet, basename='personalinfo')

# Register other views with the default router
router.register(r'skills', views.SkillViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'education', views.EducationViewSet)
router.register(r'contact', views.ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(singleton_router.urls)),
]