from .serializers import JobSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from .models import Job

class JobViewSet(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  viewsets.GenericViewSet
):
  queryset = Job.objects.all()
  serializer_class = JobSerializer
  # lookup_value_regex =  r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

  # def create(self, request):
  #   data = request.data
  #   serializer = JobSerializer(data=data)
  #   serializer.is_valid(raise_exception=True)
  #   job = serializer.save()
    
  #   return Response({'id': job.id}, status=status.HTTP_201_CREATED)
  
  # def retrieve(self, request, pk=None):
  #   job_id = pk
  #   job = Job.objects.filter(id=job_id).first()
  #   if job is None:
  #     return Response({'message': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
    
  #   return Response({'status': job.status}, status=status.HTTP_200_OK)