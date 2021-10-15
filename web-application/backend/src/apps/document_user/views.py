import uuid
# from djoser.views import UserView, UserDeleteView
from djoser import views as djoser_views
from djoser import serializers
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework import permissions
from .models import DocUser
from src.apps.otp import permissions as otp_permissions
from djoser import serializers
from django.http import JsonResponse


class DocUserLogoutAllView(views.APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocUserView(djoser_views.UserViewSet):
    """
    Uses the default Djoser view, but add the IsOtpVerified permission.
    Use this endpoint to retrieve/update user.
    """
    model = DocUser
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]


class DocUserDeleteView(djoser_views.UserViewSet):
    """
    Uses the default Djoser view, but add the IsOtpVerified permission.
    Use this endpoint to remove actually authenticated user.
    """
    serializer_class = serializers.UserDeleteSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        user_id = request.user.id
        if user_id != pk:
            print(status)
            return JsonResponse(data={"message": "Does not have access"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            object = DocUser.objects.get(pk=pk)
            if object is not None:
                object.otp = True
                serializer = serializers.UserSerializer(object, data=request.data, partial=True)
                # partial=True to update a data partially
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
                return JsonResponse(data={"message": "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)