from django import urls
from .import views
from django.contrib.auth import views as auth_view
from .forms import CustomerLogin, PasswordReset, PasswordChange, MySetPasswordForm

urlpatterns = [
    urls.path('home/', views.home, name = 'home'),

    urls.path('category/<slug:val>/', views.category, name = 'category'),

    urls.path('category-title/<val>/', views.categoryTitle, name = 'category_title'),

    urls.path('product-detail/<id>/', views.productDetail, name = 'product_detail'),

    urls.path('about/', views.about, name = 'about'),

    urls.path('contact/', views.contact, name = 'contact'),

    urls.path('profile/', views.profile, name = 'profile'),

    urls.path('address/', views.address, name = 'address'),

    urls.path('update-address/<id>/', views.updateAddress, name = 'update_address'),

    urls.path('add-to-cart/', views.addToCart, name = 'add_to_cart'),

    urls.path('carts/', views.showCart, name = 'show_cart'), 

    urls.path('check-out', views.checkOut, name = 'check_out'), 
    
    urls.path('plus-cart/', views.plusCart),

    urls.path('minus-cart/', views.minusCart),

    urls.path('remove-cart/', views.removeCart),

    urls.path('plus-wishlist/', views.plusWishlist),

    urls.path('minus-wishlist/', views.minusWishlist),

    urls.path('wishlist/', views.wishlist,name='wishlist'),

    urls.path('search/', views.search, name = 'search'),

    urls.path('orders/', views.order, name = 'orders'),

    urls.path('sign-up/', views.customerSignUp, name = 'sign_up'),
    
    urls.path('login/',auth_view.LoginView.as_view(template_name = 'login.html',authentication_form = CustomerLogin), name='login'),

    urls.path('logout/', views.custom_logout_view, name='logout'),

    urls.path('password-change/',auth_view.PasswordChangeView.as_view(template_name = 'password_change.html',form_class = PasswordChange, success_url='/password-change-done'), name='password_change'),

    urls.path('password-change-done/',auth_view.PasswordChangeDoneView.as_view(template_name = 'password_change_done.html'), name='password_change_done'),

    urls.path('password-reset/',auth_view.PasswordResetView.as_view(template_name = 'password_reset.html',form_class = PasswordReset), name='password_reset'),
    
    urls.path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name='password_reset_done'),
    
    urls.path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html', form_class = MySetPasswordForm), name='password_reset_confirm'),
    
    urls.path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name='password_reset_complete'),
]