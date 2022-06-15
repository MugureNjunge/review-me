from django.test import TestCase
from .models import *


class ProfileTestClass(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='mooh')
        self.profile = Profile.objects.create(user = self.user,bio = 'love and laugh')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile(self):
        self.profile.save()
        profile = Profile.get_profile()
        self.assertTrue(len(profile) > 0)

    def test_search_profile(self):
        self.profile.save()
        profile = Profile.search_profile('mooh')
        self.assertTrue(len(profile) > 0)
    

class ProjectTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='mooh')
        self.profile = Profile.objects.create(user = self.user,bio = 'live and laugh')

        self.project = Project.objects.create(name = self.user,profile = self.profile,title = 'Picturesque',location='Coast',description='The very best',link= 'https://picsque.herokuapp.com/')

    def test_instance(self):
        self.assertTrue(isinstance(self.project,Project))
    

    def test_get_projects(self):
        self.project.save()
        project = Project.get_projects()
        self.assertTrue(len(project) == 1)
    
    def test_save_project(self):
        self.project.save_project()
        project = Project.objects.all()
        self.assertTrue(len(project) > 0)
    
    def test_delete_project(self):
        self.project.delete_project()
        project = Project.search_by_projects('Picturesque')
        self.assertTrue(len(project) < 1)


    def test_find_project(self):
        self.project.save()
        project = Project.search_by_project('Picturesque')
        self.assertTrue(len(project) > 0)
 
class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='mooh')

        self.rating= Rating.objects.create(user= self.user, design=10, usability=10,content=10 )

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_rating(self):
        self.assertTrue(isinstance(self.rating,Rating))

    def test_get_rating(self):
        self.rating.save()
        rating = Rating.get_rating()
        self.assertTrue(len(rating) == 1)