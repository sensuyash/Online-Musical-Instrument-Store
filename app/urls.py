from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    path('', views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='show_cart'),
    path('pluscart/',views.plus_cart,name='plus_cart'),
    path('minuscart/',views.minus_cart,name='minus_cart'),
    path('removecart/',views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='/paymentdone'),
    path('nonpercussion/', views.nonpercussion,name='non_percussion'),
    path('nonpercussion/<slug:data>',views.nonpercussion,name='non_percussion-data'),
    path('percussion/', views.percussion, name='percussion'),
    path('percussion/<slug:data>', views.percussion, name='percussion-data'),
    path('guitar/', views.guitar, name='guitar'),
    path('guitar/<slug:data>', views.guitar, name='guitar-data'),
    path('voilin/', views.voilin, name='voilin'),
    path('voilin/<slug:data>', views.voilin, name='voilin-data'),
    path('melodica/', views.melodica, name='melodica'),
    path('melodica/<slug:data>', views.melodica, name='melodica-data'),
    path('keyboard/', views.keyboard, name='keyboard'),
    path('keyboard/<slug:data>', views.keyboard, name='keyboard-data'),
    path('tabla/', views.tabla, name='tabla'),
    path('tabla/<slug:data>', views.tabla, name='tabla-data'),
    path('sitar/', views.sitar, name='sitar'),
    path('sitar/<slug:data>', views.sitar, name='sitar-data'),
    path('cajonbox/', views.cajonbox, name='cajonbox'),
    path('cajonbox/<slug:data>', views.cajonbox, name='cajonbox-data'),
    path('harmonium/', views.harmonium, name='harmonium'),
    path('harmonium/<slug:data>', views.harmonium, name='harmonium-data'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/password_change.html',success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('checkout/', views.checkout, name='checkout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
