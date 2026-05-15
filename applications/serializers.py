from rest_framework import serializers
from .models import Application
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field

class ApplicationSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'company_name', 'position', 'status', 
            'applied_date', 'deadline', 'notes', 'is_overdue', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_overdue']

    @extend_schema_field(serializers.BooleanField())
    def get_is_overdue(self, obj):
        if obj.deadline:
            return obj.deadline < timezone.localdate() and obj.status != Application.Status.OFFER
        return False