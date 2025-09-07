from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.shortcuts import render
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact
from .serializers import (
    PersonalInfoSerializer, SkillSerializer, ProjectSerializer,
    ExperienceSerializer, EducationSerializer, ContactSerializer
)
from .constants import (
    API_VERSION, CONTACT_SUCCESS_MESSAGE, CONTACT_ERROR_MESSAGE
)


def home(request):
    """
    Home view for the portfolio API.
    Returns basic API information and available endpoints.
    """
    return JsonResponse({
        'message': 'Portfolio API is running!',
        'version': API_VERSION,
        'endpoints': {
            'personal_info': '/api/personal-info/',
            'skills': '/api/skills/',
            'projects': '/api/projects/',
            'experience': '/api/experience/',
            'education': '/api/education/',
            'contact': '/api/contact/',
            'admin': '/admin/',
        },
        'documentation': 'Use /admin/ to manage portfolio content'
    })


def custom_404(request, exception):
    """
    Custom 404 error handler.
    Returns JSON response for API requests, HTML for others.
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Endpoint not found',
            'message': 'The requested API endpoint does not exist',
            'available_endpoints': [
                '/api/personal-info/',
                '/api/skills/',
                '/api/projects/',
                '/api/experience/',
                '/api/education/',
                '/api/contact/',
            ]
        }, status=404)
    
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Custom 500 error handler.
    Returns JSON response for API requests, HTML for others.
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }, status=500)
    
    return render(request, '500.html', status=500)


class PersonalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for PersonalInfo model.
    Provides read-only access to personal information.
    """
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the most recent personal info.
        Returns the first (and should be only) PersonalInfo instance.
        """
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                serializer = PersonalInfoSerializer(personal_info, context={'request': request})
                return Response(serializer.data)
            return Response({'error': 'No personal information found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error retrieving personal info: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Skill model.
    Provides read-only access to skills with optional category filtering.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Filter skills by category if specified in query parameters.
        """
        queryset = Skill.objects.all()
        category = self.request.query_params.get('category', None)
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Project model.
    Provides read-only access to projects with optional featured filtering.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Filter projects by featured status if specified in query parameters.
        """
        queryset = Project.objects.all()
        featured = self.request.query_params.get('featured', None)
        
        if featured is not None:
            try:
                featured_bool = featured.lower() == 'true'
                queryset = queryset.filter(featured=featured_bool)
            except (ValueError, AttributeError):
                # If featured parameter is invalid, return all projects
                pass
        
        return queryset


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Experience model.
    Provides read-only access to work experience.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.AllowAny]


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Education model.
    Provides read-only access to educational background.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact model.
    Allows creation of contact messages and read access for admin.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Override create to handle contact form submissions with custom response.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': CONTACT_SUCCESS_MESSAGE,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': CONTACT_ERROR_MESSAGE.format(str(e))}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
