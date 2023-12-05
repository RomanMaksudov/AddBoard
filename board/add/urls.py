from django.urls import path, include
from .views import (
   PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseList, ResponseDelete, ResponseCreate,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('responses/', ResponseList.as_view(), name='responses'),
   path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
   path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
]
