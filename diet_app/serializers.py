from rest_framework import serializers

from django.shortcuts import get_object_or_404

from diet_app.models import User, UserProfile, FoodLog



class UserSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = User
        fields = ['username', 'email', 'password', 'phone', 'profile']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def get_profile(self, obj):

        try:

            profile = get_object_or_404(UserProfile, owner=obj)

            serializer_instance = UserProfileSerializer(profile)

            return serializer_instance.data
        
        except:

            return "No Profile"
    


class UserProfileSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = UserProfile
        fields = "__all__"
        read_only_fields = ['owner', 'bmr']


    def validate(self, attrs):
        return super().validate(attrs)
    


class FoodLogSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoodLog
        fields = "__all__"
        read_only_fields = ['owner', 'created_at']

