from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

admin.site.site_header = "CHMS KPI-tool"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to UMSRA Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls'))
]
