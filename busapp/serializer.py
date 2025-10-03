from busapp.models import LoginModel
from rest_framework.serializers import ModelSerializer

class LoginSerializer(ModelSerializer):
    class Meta:
        model = LoginModel
        fields = '__all__'


# class User_Serializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'