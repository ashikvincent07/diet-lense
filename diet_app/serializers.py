from rest_framework import serializers

from diet_app.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['username', 'email', 'password', 'phone']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)