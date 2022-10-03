from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    # auth
    path("auth/", account_views.Auth.as_view(), name="Auth"),
    path(
        "user/register/",
        account_views.UserRegister.as_view(),
        name="UserRegister",
    ),
    path(
        "user/list/",
        account_views.ListUser.as_view(),
        name="ListUser",
    ),
    path(
        "user/update/<int:pk>/",
        account_views.UpdateUser.as_view(),
        name="UpdateUser",
    ),
    path(
        "user/delete/<int:pk>/",
        account_views.DeleteUser.as_view(),
        name="DeleteUser",
    ),
    path(
        "qr-code",
        account_views.my_view,
        name="qr-code",
    ),
]
