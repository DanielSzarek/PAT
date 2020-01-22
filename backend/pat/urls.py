from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserCreateView.as_view()),
    path('users/set_password/', views.UserPasswordChangeView.as_view()),
    path('users/me/', views.UserDetail2View.as_view()),
    path('packs/', views.PackListView.as_view()),
    path('packs/<int:pk>', views.PackDetailView.as_view()),
    path('packs/courier/<int:pk>', views.PackCourier.as_view())
    ]
