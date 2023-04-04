from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
=======
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls'))
>>>>>>> frontend
]
