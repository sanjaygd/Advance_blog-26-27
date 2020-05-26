from django.urls import path

from .views import comment_thread,comment_delete

app_name = 'comments'
urlpatterns = [
    path('<int:id>/',comment_thread, name='thread'),
    path('delete/<int:id>/',comment_delete, name='comment_delete')
]
