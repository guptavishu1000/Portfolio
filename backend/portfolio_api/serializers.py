from rest_framework import serializers
from django.templatetags.static import static
from django.conf import settings
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact, SocialLink


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model with all fields."""
    
    class Meta:
        model = Skill
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer for SocialLink model."""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_display', 'url', 'display_text', 'icon_class', 'is_active', 'order']
        read_only_fields = ['id', 'platform_display']
        
    def create(self, validated_data):
        # Get the personal_info from the context
        personal_info = self.context.get('personal_info')
        if not personal_info:
            raise serializers.ValidationError("Personal info is required")
            
        # Create the social link with the associated personal_info
        return SocialLink.objects.create(personal_info=personal_info, **validated_data)
        
    def update(self, instance, validated_data):
        # Prevent changing the personal_info of an existing social link
        validated_data.pop('personal_info', None)
        return super().update(instance, validated_data)


class PersonalInfoSerializer(serializers.ModelSerializer):
    """Serializer for PersonalInfo model with social links."""
    profile_image_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, required=False)
    
    # Backward compatibility fields
    github_url = serializers.SerializerMethodField(required=False)
    linkedin_url = serializers.SerializerMethodField(required=False)
    leetcode_url = serializers.SerializerMethodField(required=False)
    codeforces_url = serializers.SerializerMethodField(required=False)
    kaggle_url = serializers.SerializerMethodField(required=False)
    website_url = serializers.SerializerMethodField(required=False)
    twitter_url = serializers.SerializerMethodField(required=False)
    facebook_url = serializers.SerializerMethodField(required=False)
    instagram_url = serializers.SerializerMethodField(required=False)
    youtube_url = serializers.SerializerMethodField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Build a cache of social links to avoid N+1 queries.
        """
        super().__init__(*args, **kwargs)
        self._links_cache = {}
        # 'self.instance' will be the PersonalInfo object
        if self.instance:
            # '.all()' here uses the prefetched data, NOT a new query
            for link in self.instance.social_links.all():
                if link.is_active:
                    self._links_cache[link.platform] = link.url

    class Meta:
        model = PersonalInfo
        fields = [
            'id', 'name', 'title', 'bio', 'email', 'phone', 'location',
            'github_url', 'linkedin_url', 'leetcode_url', 'codeforces_url', 'kaggle_url' , 'website_url', 'twitter_url', 'facebook_url', 'instagram_url', 'youtube_url',  # Legacy fields
            'social_links',  # New social links
            'profile_image', 'resume',
            'profile_image_url', 'resume_url',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')
    
    def get_github_url(self, obj):
        return self._get_social_link_url(obj, 'github')
        
    def get_linkedin_url(self, obj):
        return self._get_social_link_url(obj, 'linkedin')
        
    def get_leetcode_url(self, obj):
        return self._get_social_link_url(obj, 'leetcode')
    
    def get_codeforces_url(self, obj):
        return self._get_social_link_url(obj, 'codeforces')
    
    def get_kaggle_url(self, obj):
        return self._get_social_link_url(obj, 'kaggle')
        
    def get_website_url(self, obj):
        return self._get_social_link_url(obj, 'website')
        
    def get_twitter_url(self, obj):
        return self._get_social_link_url(obj, 'twitter')
        
    def get_facebook_url(self, obj):
        return self._get_social_link_url(obj, 'facebook')
        
    def get_instagram_url(self, obj):
        return self._get_social_link_url(obj, 'instagram')
        
    def get_youtube_url(self, obj):
        return self._get_social_link_url(obj, 'youtube')

    def _get_social_link_url(self, obj, platform):
        social_link = obj.social_links.filter(platform=platform, is_active=True).first()
        return social_link.url if social_link else ''

    def _abs(self, request, path):
        """Build absolute URL if request present, else return path."""
        if request:
            return request.build_absolute_uri(path)
        # If no request (unlikely in DRF), return a relative path
        return path

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        # If an uploaded file exists, return its URL
        if getattr(obj, 'profile_image', None) and getattr(obj.profile_image, 'url', None):
            return self._abs(request, obj.profile_image.url)
        # Fallback to static asset
        static_path = settings.STATIC_URL.rstrip('/') + '/assets/images/profile_pic.png'
        return self._abs(request, static_path)

    def get_resume_url(self, obj):
        request = self.context.get('request')
        if getattr(obj, 'resume', None) and getattr(obj.resume, 'url', None):
            return self._abs(request, obj.resume.url)
        static_path = settings.STATIC_URL.rstrip('/') + '/assets/docs/Vishesh_Gupta_Resume.pdf'
        return self._abs(request, static_path)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model with nested technologies."""
    technologies = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience model with nested technologies."""
    technologies_used = SkillSerializer(many=True, read_only=True)
    company_logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = ['id', 'company', 'company_logo', 'company_logo_url', 'position', 'location',
                 'start_date', 'end_date', 'current', 'description', 'achievements', 'technologies_used']
    
    def get_company_logo_url(self, obj):
        if obj.company_logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.company_logo.url) if request else obj.company_logo.url
        return None


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for Education model."""
    institution_logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Education
        fields = ['id', 'institution', 'institution_logo', 'institution_logo_url', 'degree', 
                 'field_of_study', 'start_date', 'end_date', 'current', 'description', 'cpi']
    
    def get_institution_logo_url(self, obj):
        if obj.institution_logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.institution_logo.url) if request else obj.institution_logo.url
        return None


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model with all fields."""
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('created_at', 'read') 