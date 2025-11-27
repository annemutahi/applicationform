from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('submit/', views.submit_response, name='submit_response'),
    path('get-departments/<int:center_id>/', views.get_departments, name='get_departments'),
    path('success/', views.success_page, name='success'),
    path('dashboard/login/', views.admin_login, name='admin_login'),
    path('dashboard/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/responses/', views.admin_responses_list, name='admin_responses_list'),
    path('dashboard/responses/<int:response_id>/', views.admin_response_detail, name='admin_response_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)