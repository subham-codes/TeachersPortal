from django.urls import path
from . import views

app_name = 'student_listing'

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('register/',views.register, name='register'),
    path('delete_student/<int:id>/',views.delete_student, name='delete_student'),
    path('update_student/<int:id>/',views.update_student, name='update_student'),
]
