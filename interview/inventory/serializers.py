from rest_framework import serializers

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


class InventoryTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InventoryTag
        fields = ['id', 'name', 'is_active']
        
        
class InventoryLanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InventoryLanguage
        fields = ['id', 'name']


class InventoryTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InventoryType
        fields = ['id', 'name']


class InventorySerializer(serializers.ModelSerializer):
    type = InventoryTypeSerializer()
    language = InventoryLanguageSerializer()
    tags = InventoryTagSerializer(many=True)
    metadata = serializers.JSONField()
    
    class Meta:
        model = Inventory
        fields = ['id', 'name', 'type', 'language', 'tags', 'metadata']

class InventoryDateCreatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ["id", "name", "type", "language", "tags", "metadata", "created_at"]


class DateSerializer(serializers.Serializer):
    date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

