from field_workers.models import FieldWorker
from rest_framework import serializers


class FieldWorkersSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldWorker
        fields = ('id', 'first_name', 'last_name', 'function', 'created_at')

    def update(self, worker, validated_data):
        worker.first_name = validated_data.get('first_name', worker.first_name)
        worker.last_name = validated_data.get('last_name', worker.last_name)
        worker.function = validated_data.get('function', worker.function)
        worker.save()
        return worker
