from django.urls import path
from .views import *


urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/create', PostCreate.as_view(), name='post_create_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete', PostDelete.as_view(), name='post_delete_url'),
    path('post/<slug:slug>/comment/', PostDetail.as_view(), name='add_comment'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete', TagDelete.as_view(), name='tag_delete_url'),
    path('authentification/', authentification, name='authentification_url'),
    path('register/', RegisterUser.as_view(), name='registration_url'),
    path('login/', LoginUser.as_view(), name='login_url'),
    path('logout_confirm/', logout_confirm, name='logout_confirm_url'),
    path('logout/', logout_user, name='logout_url'),
]
