
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from movies_app.api.serializers import MovieRateSerializer, MovieRateSerializer2, MovieSerializer
from movies_app.models import Rate, Movie

from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from movies_app.api.permissions import IsAuthenticatedOrReadOnlyCustom
from rest_framework.authentication import TokenAuthentication


class ExampleViewset(viewsets.ReadOnlyModelViewSet):

    queryset = Rate.objects.all()
    serializer_class = MovieRateSerializer
    authentication_classes = (TokenAuthentication,)

class MovieViewset(viewsets.ModelViewSet):

    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication,)

    serializer_class = {
        'rate': MovieRateSerializer,
        'default': MovieSerializer
    }
    permission_classes = [DjangoModelPermissions,]


    def get_serializer_class(self):
        return self.serializer_class[self.action] if self.action in self.serializer_class.keys() else \
        self.serializer_class['default']

    def get_serializer_context(self):
        context = super(MovieViewset, self).get_serializer_context()
        context.update({'request':self.request})
        return context

    @action(methods=['POST'],detail=True)
    def rate(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=obj, user=request.user)
        return Response(data=self.get_serializer(serializer.instance).data)

# class RateViewSet(viewsets.ModelViewSet):
#     queryset = Rate.objects.all()
#     serializer_class = MovieRateSerializer2
#
#
# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#     def rate(self, request):
#         obj = self.get_object()
#         try:
#             Rate.objects.create(rate=request.data.get('rate'), movie=obj, user=request.user)
#         except:
#             return Response({'error': f'can not crcreate '})

#class ExampleViewset(viewsets.ViewSet):
    # model = Rate
    # serializer_class = MovieRateSerializer2
    #
    # def get_queryset(self):
    #     _filter = {}
    #     if 't' in self.request.query_params.keys():
    #         _filter.update({'movie__title__icontains': self.request.query_params.get('t')})
    #     if 'u' in self.request.query_params.keys():
    #         _filter.update({'user__username__icontains': self.request.query_params.get('u')})
    #     return self.model.objects.filter(**_filter)

    # def get_object(self, pk):
    #     return get_object_or_404(self.get_queryset(), pk=pk)

    # def get_serializer(self, query, many=False):
    #     return MovieRateSerializer2(query, many=many, context={'request': self.request})

    # def list(self, request):
    #     qs = self.get_queryset()
    #     return Response({'data': self.get_serializer(qs, many=True).data})

    # def retrieve(self, request, pk=None):
    #     return Response(data=self.get_serializer(self.get_object(pk)).data)
    #
    # def create(self, request):
    #     return Response({'action': 'create'})

    # def update(self, request, pk=None):
    #     return Response({'action': 'update'})
    #
    # def partial_update(self, request, pk=None):
    #     return Response({'action': 'partial update'})
    #
    # def destroy(self, request, pk=None):
    #     obj = self.get_object(pk)
    #     obj.delete()
    #     return Response(data={'done': 'ok'}, status=HTTP_200_OK)