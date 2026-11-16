from rest_framework import serializers
from .models import Job
import json

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = ['id', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at', 'picked_up_at', 'error', 'retries', 'max_retry', 'payload', 'job_type']
    read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at', 'picked_up_at', 'error', 'retries', 'max_retry']
  def validate_payload(self, value):
    from config.settings import MAX_BYTES
    if not isinstance(value, dict):
      raise serializers.ValidationError("Payload must be a valid dict")
    
    payload_size = len(json.dumps(value).encode('utf-8'))
    if payload_size >= MAX_BYTES:
      raise serializers.ValidationError('Payload must be less than 100kb')
    
    return value