
from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name ="home"),
   path('contact/',views.contact, name ="contact"),
   path('checkout/',views.checkout, name ="checkout"),
   path('shop/',views.shop, name ="shop"),
   
   path('login/',views.login_user, name ="login"),
   path('logout/',views.logout_user, name ="logout"),
   path('register/', views.register_user, name ="register"),
   path('detail/<int:pk>',views.detail, name ="detail"),


   path('cart_summary/',views.cart_summary, name ="cart_summary"),
   path('update_item/',views.updateItem, name ="update_item"),
   path('payment/',views.payment, name ="payment"),
]
