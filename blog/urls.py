from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import FilterBaseViewPost
from .views import MainPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('posts/',include('posts.urls')),
    path('', FilterBaseViewPost.as_view(), name="filter"),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
