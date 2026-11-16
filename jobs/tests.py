from rest_framework import status
from rest_framework.test import APITestCase
from .models import Job
from config.settings import MAX_BYTES

class JobSubmitTests(APITestCase):
  def test_valid_submit_creates_queued_job(self):
    response = self.client.post(
      '/api/jobs/',
      {'job_type': 'mock_task', 'payload': {'seconds': 2}},
      format='json',
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    job = Job.objects.get(pk=response.data['id'])
    self.assertEqual(job.status, Job.JOB_STATES.QUEUED)
    
  def test_create_job_with_status_and_retries_creates_queued_job_with_zero_retires(self):
    response = self.client.post(
      '/api/jobs/',
      {'job_type': 'mock_task', 'payload': {'seconds': 2}, 'status': 'completed', 'retries': 99},
      format='json',
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    job = Job.objects.get(pk=response.data['id'])
    self.assertEqual(job.status, Job.JOB_STATES.QUEUED)
    self.assertEqual(job.retries, 0)
    
  def test_create_job_without_job_type_returns_400(self):
    response = self.client.post(
      '/api/jobs/',
      {'payload': {'seconds': 2}},
      format='json',
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_create_job_with_unknown_job_type_returns_400(self):
    response = self.client.post(
      '/api/jobs/',
      {'payload': {'seconds': 2}, 'job_type': 'rm_rf'},
      format='json',
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_get_job_returns_200(self):
    new_job = self.client.post(
      '/api/jobs/',
      {'job_type': 'mock_task', 'payload': {'seconds': 2}},
      format='json',
    )
    id = new_job.data['id']
    response = self.client.get(
      f'/api/jobs/{id}/'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['status'], Job.JOB_STATES.QUEUED)
    
  def test_get_job_with_unknown_uuid_returns_404(self):
    response = self.client.get(
      '/api/jobs/4edc71cb-3fb8-4abc-bbbf-0a433b486c27/'
    )
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
  def test_get_job_with_malformed_uuid_returns_404(self):
    response = self.client.get(
      '/api/jobs/abc/'
    )
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
  def test_payload_round_trips_exactly(self):
    payload = {
      'seconds': 2,
      'recipients': ['a@example.com', 'b@example.com'],
      'options': {'urgent': True, 'note': None},
    }
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': payload}, format='json'
    )
    job = Job.objects.get(pk=response.data['id'])
    self.assertEqual(job.payload, payload)
    
  def test_create_job_with_string_payload_fails(self):
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': 'hello'}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_create_job_with_list_payload_fails(self):
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': [1,2,3]}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_create_job_with_large_payload_fails(self):
    large_dict = {"data": "a" * MAX_BYTES}
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': large_dict}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_create_job_with_payload_just_under_limit_fails(self):
    size = 1024 - 15
    large_dict = {"data": "a" * size}
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': large_dict}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
  def test_create_job_with_payload_at_the_limit_fails(self):
    size = MAX_BYTES - 12
    large_dict = {"data": "a" * size}
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task', 'payload': large_dict}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_create_job_with_missing_payload_passes(self):
    response = self.client.post(
      '/api/jobs/', {'job_type': 'mock_task'}, format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    job = Job.objects.get(pk=response.data['id'])
    self.assertEqual(job.status, Job.JOB_STATES.QUEUED)
    self.assertEqual(job.payload, {})