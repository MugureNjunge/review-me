from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver


class Profile(models.Model):
    profile_pic= CloudinaryField('image')
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=100,blank=True)
    bio= models.TextField()

    def save_profile(self):
        self.save()

    def __str__(self):
        return self.fullname

    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile

    def delete_profile(self):
         self.delete()

    def save_profile(self):
        self.save() 

    @classmethod
    def search_by_user(cls, user):
        projects = cls.objects.filter(user=user)
        return projects  
    
class Project(models.Model):
    title= models.CharField(max_length=100)
    project_image= CloudinaryField('image')
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    description= models.TextField()
    link= models.CharField(max_length=250)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title + '' + self.description
    
    def save_project(self):
        self.save()

    @classmethod
    def search_by_projects(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects
    
    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()


    @classmethod
    def get_projects_by_profile(cls, profile):
        projects = Project.objects.filter(profile__pk=profile)
        return projects
    

class Rating(models.Model):
    design = models.IntegerField(blank=True,default=0)
    usability = models.IntegerField(blank=True,default=0)
    content = models.IntegerField(blank=True,default=0)
    votes = models.IntegerField(blank=True,default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)        




