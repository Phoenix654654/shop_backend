from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.views.user import UserViewSet, UserMeView, UserActionViewSet

router = DefaultRouter()

router.register('user', UserViewSet)
urlpatterns = [
    path('auth/user/me/', UserMeView.as_view()),
    path('user/<int:pk>/block/', UserActionViewSet.as_view({'post': 'block'}), ),
    path('user/<int:pk>/unblock/', UserActionViewSet.as_view({'post': 'unblock'}), ),
]
urlpatterns += router.urls
