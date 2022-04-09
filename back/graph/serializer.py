
from rest_framework import serializers
from .models import Graph


class GraphSeriarizer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = ["pk", "title", "graph", "tags"]
        read_only_fields = ('created_at', 'updated_at')
