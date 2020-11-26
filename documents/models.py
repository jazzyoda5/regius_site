from django.db import models
from projects.models import Project

class DocumentTemplate(models.Model):

    document = models.FileField(upload_to='media')
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.document.storage.delete(self.document.name)
        super().delete()


class ProjectDocument(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_doc = models.FileField(upload_to='media')
    title = models.CharField(max_length=50)

    def delete(self, using=None, keep_parents=False):
        self.project_doc.storage.delete(self.project_doc.name)
        super().delete()
