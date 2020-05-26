from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include


from accounts.views import login_view,register_view,logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('blog_app.urls', namespace='posts')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout',logout_view,name='logout')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)