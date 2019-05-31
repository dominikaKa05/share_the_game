"""share_the_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from sharing_app import views
from share_the_game import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPageView.as_view(), name = 'main_page'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), {'template_name': '/logout.html'},name= 'logout'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search/',views.ProductSearchListView.as_view(), name='product_search'),
    path('add/',views.ProductAddView.as_view(), name='product_add'),
    # path('add/',views.ProductCreate.as_view(), name='product_add'),
    path('search/<int:object_id>/detail/', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('profile/', views.ProfileView.as_view(), name = 'profile_view'),
    path('search/<int:object_id>/collection/',views.AddToCollectionView.as_view(), name='add_to_collection'),
    path('search/<int:object_id>/borrow/',views.BorrowProductView.as_view(), name ='borrow_product'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)