from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('submit-assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('view-submissions/<int:user_id>/', views.view_submissions, name='view_submissions'),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

