from rest_framework import serializers
from .models import PersonalInfo, Skill, Project, Experience, Education, Contact


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model with all fields."""
    
    class Meta:
        model = Skill
        fields = '__all__'


class PersonalInfoSerializer(serializers.ModelSerializer):
    """Serializer for PersonalInfo model with all fields."""
    
    class Meta:
        model = PersonalInfo
        fields = '__all__'


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