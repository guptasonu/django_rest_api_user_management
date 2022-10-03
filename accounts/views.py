import random
import string

import qrcode
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from qr_code.qrcode.utils import QRCodeOptions
from rest_framework import filters, generics, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from accounts import models as account_models
from accounts import user_serializers


# Create your views here.
class Auth(ObtainAuthToken):

    serializer_class = user_serializers.BasicAuthenticationSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="This Api is used to Authenticate the Apis",
        operation_description="Fill Username and Password and get one token use it to authention for apis",
    )
    def post(self, request, *args, **kwargs):
        """ """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"].first()

        token = account_models.Token.objects.create(user=user)
        serializer = user_serializers.UserSerializer(user)
        return Response(
            {
                "token": token.key,
                "user": serializer.data,
            }
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="This Api is used to Create New user",
        operation_description="Create A new user using this Apis",
    ),
)
class UserRegister(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = user_serializers.UserSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="This Api is used to get all Created user",
        responses={200: user_serializers.UserSerializer(many=True)},
    ),
)
class ListUser(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = account_models.User.objects.all()
    serializer_class = user_serializers.UserSerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_summary="This Api is used to Update Created user",
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="This Api is used to Partical Update Created user",
    ),
)
class UpdateUser(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = account_models.User.objects.all()
    serializer_class = user_serializers.UpdateUserSerializer


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_summary="This Api is used to Delete Created user",
    ),
)
class DeleteUser(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = account_models.User.objects.all()
    serializer_class = user_serializers.UserSerializer


@api_view(("GET",))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def my_view(request):
    # Build context for rendering QR codes.
    qr_text = create_random_token()
    print("qr_text: ", qr_text)
    context = dict(
        my_options=QRCodeOptions(size="M", border=6, error_correction="L"),
        qr_text=qr_text,
    )

    # Render the view.
    # return render(request, "accounts/index.html", context=context)
    return Response(
        {
            "qr_text": qr_text,
        },
        template_name="accounts/index.html",
    )


def create_random_token():

    first_string = "".join(
        random.choices(f"+/{string.digits}{string.ascii_letters}", k=78)
    )

    last_string = "".join(
        random.choices(f"+/{string.digits}{string.ascii_letters}", k=43)
    )

    static_string = "Rq3vHQesnBqjMYo6UONFYVgHBp03cWejGw5mhzn0x30=,cFsIETj61xAd9+6iom5OSxoSEDFT55oeUAocB1GEplw=,"
    return f"2@{first_string}==,{static_string}{last_string}="
    # print("final_string: ", final_string)

    # img = qrcode.make(final_string)
    # type(img)  # qrcode.image.pil.PilImage
    # img.save("some_file.png")
