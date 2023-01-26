from django.urls import path

from api.views import UserRegisterViewSet, UrlRegisterViewSet, WarningViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    ##### AUTH #####
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegisterViewSet.as_view({'post':'register'}), name='user_register'),
    ##### URL #####
    path('url/', UrlRegisterViewSet.as_view({'put':'create', 'get':'list'}), name='url'),
    path('url/<int:pk>', UrlRegisterViewSet.as_view({'get':'retrieve', 'delete':'delete'}), name='url'),
    path('url/<int:pk>/reset', UrlRegisterViewSet.as_view({'post':'reset_warnings'}), name='url'),
    ##### WARNING #####
    path('warning/', WarningViewset.as_view({'get':'list'}), name='warning'),
]