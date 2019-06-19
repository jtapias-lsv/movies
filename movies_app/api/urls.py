from django.urls import path

from movies_app.api.viewsets import RateViewSet, ExampleViewset, MovieViewSet

urlpatterns = [
    # path('movie/', ExampleViewset.as_view({'get': 'list', 'post': 'create'}), name='movie-list-actions'),
    path('movierate/', RateViewSet.as_view({'get': 'list', 'post': 'create'}), name='movierate-list-actions'),
    path('movierate/<int:pk>/',
         RateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}),
         name='movierate-detail-actions'),
    path('movie/', MovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-list-actions'),
    path('movie/<int:pk>/',
         MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}),
         name='movie-detail-actions'),
    path('movie-example/', ExampleViewset.as_view({'get': 'list', 'post': 'create'}), name='m-e-l-a'),
    path('movie-example/<int:pk>/',
         ExampleViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}),
         name='m-e-d-a'),
]