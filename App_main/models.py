from django.db import models
from App_auth.models import User

# Create your models here.
t_status = (
    ('Assigned', 'Assigned'),
    ('Pending', 'Pending'),
    ('Started', 'Started'),
    ('Completed', 'Completed'),
)


class ProjectModel(models.Model):
    task_name = models.CharField(max_length=150)
    work_overview = models.TextField(blank=True)
    work_file = models.FileField(blank=True, null=True, upload_to='TaskFile/')
    assigned_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_by')
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_to')
    deadline = models.DateTimeField(blank=True, null=True)
    task_status = models.CharField(max_length=50, choices=t_status)

    def __str__(self):
        return f"{self.task_name}-{self.deadline}"
