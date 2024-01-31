from django.urls import path
from app import views
from app.views import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import LoginForm,MyPasswordchangeField,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_to_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    
         
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.Laptop, name='laptop'),
    path('laptop/<slug:data>', views.Laptop, name='laptopdata'),
    path('bottomwear/', views.Bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.Bottomwear, name='bottomdata'),
    path('topwear/', views.Topwear, name='topwear'),
    path('topwear/<slug:data>', views.Topwear, name='topdata'),
    path('kurti/', views.Kurti, name='kurti'),
    path('kurti/<slug:data>', views.Kurti, name='kurtidata'),
    path('shoes/', views.shoes, name='shoes'),
    path('shoes/<slug:data>', views.shoes, name='shoesdata'),
    
    
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordchangeField, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    
    
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
