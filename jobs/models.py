from django.db import models
import uuid


class Job(models.Model):
  class JOB_STATES(models.TextChoices):
    QUEUED = 'queued', 'Queued'
    RUNNING = 'running', 'Running'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    RETRY_SCHEDULED = 'retry_scheduled', 'Scheduled for Retry'
    
  class JOB_TYPES(models.TextChoices):
    SEND_EMAIL = 'send_email', 'Send Email Task'
    GENERATE_REPORT = "generate_report", 'Generate Report Task'
    RESIZE_IMAGE = 'resize_image', 'Resize Image Task'
    SEND_NOTIFICATION = 'send_notification', 'Send Notification Task'
    EXPORT_CSV = 'export_csv', 'Export CSV Task'
    MOCK_TASK = 'mock_task', 'Mock Task'
    
  id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  status: str = models.CharField(max_length=100, null=False, blank=False, choices=JOB_STATES.choices, default=JOB_STATES.QUEUED)
  created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
  updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
  started_at: models.DateTimeField | None = models.DateTimeField(blank=True, null=True)
  ended_at: models.DateTimeField | None = models.DateTimeField(blank=True, null=True)
  picked_up_at: models.DateTimeField | None = models.DateTimeField(blank=True, null=True)
  error: str | None = models.TextField(null=True, blank=True)
  retries: int = models.PositiveSmallIntegerField(default=0)
  max_retry: int = models.PositiveSmallIntegerField(default=3)
  payload: dict = models.JSONField(default=dict, blank=True)
  job_type: str = models.CharField(max_length=250, null=False, blank=False, choices=JOB_TYPES.choices)
  
  def __str__(self):
    return f"{self.job_type} - {self.id} ({self.status})"