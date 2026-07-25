from rest_framework import serializers

class PredictSerializer(serializers.Serializer):
    Flats = serializers.IntegerField(default=0)
    Plots = serializers.IntegerField(default=0)
    Commercial = serializers.IntegerField(default=0)
    # Add any other feature fields your model expects here!