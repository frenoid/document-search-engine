
from djoser import serializers
from .models import DocUser


class CurrentUserSerializer(serializers.UserSerializer):

    class Meta(serializers.UserSerializer.Meta):
        model = DocUser
        fields = (
            'id',
            'email',
            'otp',
            'last_login',
        )



