from django.test import TestCase
from .models import *


class ProfileTestClass(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='mooh')
        self.profile = Profile.objects.create(user = self.user,bio = 'Life is a dream',location= 'Coast')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

class ProjectTest(TestCase):
        
    def test_save_project(self):
        self.project.save_project()
        project = Project.objects.all()
        self.assertTrue(len(project) > 0)

class RatingTest(TestCase):
        
    def test_save_project(self):
        self.project.save_project()
        project = Project.objects.all()
        self.assertTrue(len(project) > 0)
