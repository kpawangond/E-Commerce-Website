
from django.contrib import admin
from django.urls import path
from EshopApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('contact/',contact,name='contact'),
    path('terms_conditions/',terms_conditions,name='terms_conditions'),
    path('privacy_policy/',privacy_policy,name="privacy_policy"),
    path('products/',products,name="products"),
    path('admin-login/', adminLogin, name="admin_login"),
    path('cart_pk/',cart_ok,name='cart_pk'),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view_category/',view_category,name="view_category"),
    path('edit-category/<int:pk>/',update_category,name='update_category'),
    path('delete-category/<int:pk>/',delete_category,name='delete_category'),
    path('add-product/',add_product,name='add_product'),
    path('view_product/',view_product,name="view_product"),
    path('details-product/<int:pk>/',details_product,name="details_product"),
    path('update-product/<int:pk>/',update_product,name="update_product"),
    path('delete-product/<int:pk>/',delete_product,name="delete_product"),
    path('register/',registration,name='register'),
    path('login/',user_login,name="login"),
    path('user_profile/',user_profile,name="user_profile"),
    path('logout/',logoutuser,name="logout"),
    path('change-password/',change_password,name='change_password'),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('profile/', profile, name="profile"),
    path('payment/', payment, name="payment"), 
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

