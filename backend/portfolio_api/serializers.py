from rest_framework import serializers
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model with all fields."""
    
    class Meta:
        model = Skill
        fields = '__all__'


class PersonalInfoSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInfo
        fields = [
            'id', 'name', 'title', 'bio', 'email', 'phone', 'location',
            'github', 'linkedin', 'twitter', 'website',
            'profile_image', 'resume',
            'profile_image_url', 'resume_url',
            'created_at', 'updated_at',
        ]

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
    
    class Meta:
        model = Experience
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for Education model with all fields."""
    
    class Meta:
        model = Education
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model with all fields."""
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('created_at', 'read') 