from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from common.custom_permissions import IsAuthor
from common.utility import send_email, generate_code
from register.models import User, Profile
from register import serializers
from news.serializers import PostSerializer


class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny, )


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny, )


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    queryset = User.objects.all()


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = serializers.LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            token.blacklist()
            data = {
                'success': True,
                'message': "you're logged out successfully.",
                'status': status.HTTP_205_RESET_CONTENT
            }
            return Response(data)
        except TokenError:
            return Response({"message": "Invalid token", "status": status.HTTP_400_BAD_REQUEST})


class ForgotPasswordAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        code = generate_code()
        send_email(code=code, email=user.email)
        return Response({
            'success': True,
            'message': "The verification code has been successfully sent to your email",
            'email': user.email,
            'verification_type': user.codes.verify_type.TO_CONFIRM,
            'access': user.token(['access']),
            'refresh': user.token(['refresh'])
        })


class ProfileListsAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.all()
        serializer = serializers.ProfileSerializer(profile, many=True)

        data = []
        for profile_data in serializer.data:
            profile = {
                'full_name': profile_data['full_name'],
                'image': profile_data['image'],
                'job_title': profile_data['job_title']
            }
            data.append(profile)
        return Response(data, status=200)


class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'pk'


class UserProfilePostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(id=user_id, is_admin=True)
        return user.posts.all()


class ProfileEditAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthor, ]
