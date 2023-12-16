from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import cars_view, view_id_car, new_car_view, login_user, submit_login
from django.views.generic import RedirectView


urlpatterns = [
  path('admin/', admin.site.urls),
  path('cars/', cars_view, name='cars_list'),
  path('', RedirectView.as_view(url='/cars')),
  path('cars/<int:id>/', view_id_car),
  path('login/new_car/', new_car_view, name='new_car'),
  path('login/', login_user, name='login'),
  path('login/submit', submit_login),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
