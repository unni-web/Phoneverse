"""
URL configuration for phoneverse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('iphone/',views.iphone),
    path('cart/', views.cart_view, name='cart_view'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),

    path('samsung/',views.samsung),
    path('pixel/',views.pixel),
    path('account/',views.account),
    path('register/',views.register),
    path('login/',views.loginuser),
    path('logout/',views.logoutuser),
    path('adminlogin/', views.adminlogin),
    path('adminpage/', views.adminpage),
    path('addproduct/', views.addproduct),
    path('viewproduct/', views.viewproduct),
    path('update/<int:pk>',views.viewproductupdate, name='update'),
    path('delete/<int:pk>', views.viewproductdelet, name='delete'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('category/<str:category>/', views.category_view_samsung, name='category'),
    path('category/<str:category>/', views.category_view_pixel, name='category')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)