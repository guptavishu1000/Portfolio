from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.shortcuts import render
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact
from .serializers import (
    PersonalInfoSerializer, SkillSerializer, ProjectSerializer,
    ExperienceSerializer, EducationSerializer, ContactSerializer,
    SocialLinkSerializer
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


class PersonalInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PersonalInfo model.
    Provides CRUD operations for personal information.
    """
    # Use prefetch_related to solve the N+1 query problem
    queryset = PersonalInfo.objects.prefetch_related('social_links')
    serializer_class = PersonalInfoSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        """Add personal_info to the serializer context."""
        context = super().get_serializer_context()
        if self.action in ['create', 'update', 'partial_update']:
            # For update/partial_update, get the existing instance
            # For create, this will be handled in the create method
            if self.action != 'create':
                context['personal_info'] = self.get_object()
        return context
    
    def create(self, request, *args, **kwargs):
        # Create the personal info first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the created instance and update context for social links
        instance = serializer.instance
        context = self.get_serializer_context()
        context['personal_info'] = instance
        
        # Handle social links if provided
        social_links_data = request.data.get('social_links', [])
        if social_links_data:
            social_links_serializer = SocialLinkSerializer(
                data=social_links_data,
                many=True,
                context=context
            )
            social_links_serializer.is_valid(raise_exception=True)
            social_links_serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Update the context with the instance
        context = self.get_serializer_context()
        context['personal_info'] = instance
        
        # Update the personal info
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Handle social links if provided
        if 'social_links' in request.data:
            social_links_data = request.data['social_links']
            
            # Get existing social links to update or delete
            existing_links = {str(link.id): link for link in instance.social_links.all()}
            updated_link_ids = set()
            
            # Update or create social links
            for link_data in social_links_data:
                link_id = link_data.get('id')
                if link_id and link_id in existing_links:
                    # Update existing link
                    link = existing_links[link_id]
                    link_serializer = SocialLinkSerializer(
                        link,
                        data=link_data,
                        partial=partial,
                        context=context
                    )
                    link_serializer.is_valid(raise_exception=True)
                    link_serializer.save()
                    updated_link_ids.add(link_id)
                else:
                    # Create new link
                    link_data['personal_info'] = instance.id
                    link_serializer = SocialLinkSerializer(
                        data=link_data,
                        context=context
                    )
                    link_serializer.is_valid(raise_exception=True)
                    link_serializer.save()
            
            # Delete links that weren't included in the update
            for link_id, link in existing_links.items():
                if link_id not in updated_link_ids:
                    link.delete()
        
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the most recent personal info.
        Returns the first (and should be only) PersonalInfo instance.
        """
        personal_info = self.get_queryset().first() 
        
        if personal_info:
            # self.get_serializer() automatically passes the request
            # context, so your SerializerMethodFields will work.
            serializer = self.get_serializer(personal_info)
            return Response(serializer.data)
        
        # This is correct: if no info, return 404.
        return Response(
            {'error': 'No personal information found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

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
