from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import  NewCarView, CarsListView, CarDetailView, CarUpdateView
from django.views.generic import RedirectView
from accounts.views import register_view, login_view, logout_view
from django.contrib.auth.decorators import login_required



urlpatterns = [
  path('admin/', admin.site.urls),
  path('cars/', CarsListView.as_view(), name='cars_list'),
  path('register/', register_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('', RedirectView.as_view(url='/cars')),
  path('cars/<int:pk>/', CarDetailView.as_view(), name='id_car'),
  path('login/new_car/', login_required(NewCarView.as_view(), login_url='login'), name='new_car'),
  path('cars/<int:pk>/update/', login_required(CarUpdateView.as_view(), login_url='login'), name='update_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
