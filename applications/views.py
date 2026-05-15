from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action 
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend 
from django.db.models import Count 

from .models import Application
from .serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):

    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status'] 
    search_fields = ['company_name', 'position'] 
    ordering_fields = ['applied_date', 'created_at'] 

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user_apps = self.get_queryset()
        counts = user_apps.values('status').annotate(total=Count('status'))
        result = {item['status']: item['total'] for item in counts}
        result['total_all'] = user_apps.count()
        return Response(result)