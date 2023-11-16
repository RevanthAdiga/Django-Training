import structlog
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.serializers import RegistrationSerializer

logger = structlog.get_logger(__name__)


class RegisterUser(APIView):

    """Api endpoint for registering users.

    Returns:
        user data with username, email and token.

    Request:
        Object with username, email,  password and password2 keys.
    """

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: RegistrationSerializer},
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        logger.bind(
            app_name="user_app", method_name="post_registration", serializer=serializer
        )

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Registration Successful!"
            data["username"] = account.username
            data["email"] = account.email

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
