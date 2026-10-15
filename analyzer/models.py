from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company}"

class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    match_percentage = models.IntegerField(default=0)
    found_skills = models.TextField(blank=True)      # comma-separated
    missing_skills = models.TextField(blank=True)    # comma-separated
    sections_found = models.TextField(blank=True)    # comma-separated
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] 
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return f"{self.job_title} ({self.match_percentage}%)"

    def found_list(self):
        return [s for s in self.found_skills.split(',') if s]

    def missing_list(self):
        return [s for s in self.missing_skills.split(',') if s]

    def sections_list(self):
        return [s for s in self.sections_found.split(',') if s]
    
