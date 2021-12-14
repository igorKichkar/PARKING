from django.urls import path
from django.conf.urls.static import static
from test_project import settings
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('parking-manager/<str:day>/<str:place_number>/', parking_manager, name='parking_manager'),
    path('edit-space/', edit_space, name='edit_space'),
    path('edit-parking-lots/<str:rezerv>/', edit_parking_lots, name='edit_parking_lots'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('delete_space/<str:place_number>/', delete_space, name='delete_space'),
    path('delete_rezerv/<int:place_number>/', delete_rezerv, name='delete_rezerv'),
    path('parking-lots/', parking_lots, name='parking_lots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
