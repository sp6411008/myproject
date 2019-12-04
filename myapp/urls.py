from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('fashion/',views.fashion,name='fashion'),
    path('electronics/',views.electronics,name='electronics'),
    path('home_appliance/',views.home_appliance,name='home_appliance'),
    path('sale/',views.sale,name='sale'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('detail/<int:pk>/',views.detail,name='detail'),
    path('add_cart/<int:pk1>/<int:pk2>/',views.add_cart,name='add_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),
    path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),
    path('validate_otp/',views.validate_otp,name='validate_otp'),
    path('resend/',views.resend,name='resend'),
    path('enter_email/',views.enter_email,name='enter_email'),
    path('validate_password_OTP/',views.validate_password_OTP,name='validate_password_OTP'),
    path('change_password/',views.change_password,name='change_password'),
    path('profile/',views.profile,name="profile"),
    path('profile_update/',views.profile_update,name="profile_update"),
    path('change_user_password/',views.change_user_password,name='change_user_password'),
]