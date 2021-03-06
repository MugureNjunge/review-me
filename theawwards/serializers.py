from rest_framework import serializers
from .models import Profile ,Project

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=('fullname','bio','profile_pic','user')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('title','project_image','profile','description', 'link')        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('design','usability','content','overall_score', 'project', 'profile')        
