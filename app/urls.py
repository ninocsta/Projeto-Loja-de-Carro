from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import cars_view, view_id_car, new_car_view
from django.views.generic import RedirectView
from accounts.views import register_view, login_view, logout_view



urlpatterns = [
  path('admin/', admin.site.urls),
  path('cars/', cars_view, name='cars_list'),
  path('register/', register_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('', RedirectView.as_view(url='/cars')),
  path('cars/<int:id>/', view_id_car),
  path('cars/<int:id>/contato/', view_id_car, name='contato'),
  path('login/new_car/', new_car_view, name='new_car'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
