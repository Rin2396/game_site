from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication

from .forms import Registration
from .models import Club, BoardGame, GameSet, Address, Genre
from .serializers import ClubSerializer, BoardGameSerializer, GameSetSerializer, AddressSerializer, GenreSerializer


def home(request):
    return render(
        request,
        'index.html',
        {
            'clubs': Club.objects.count(),
            'boardgames': BoardGame.objects.count(),
            'genres': Genre.objects.count(),
            'gamesets': GameSet.objects.count(),
            'addresses': Address.objects.count(),
        }
    )

def create_list_view(model_class, plural_name, template):
    class CustomListView(ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            books = model_class.objects.all()
            paginator = Paginator(books, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

СlubListView = create_list_view(Club, 'clubs', 'catalog/clubs.html')
BoardGameListView = create_list_view(BoardGame, 'boardgames', 'catalog/boardgames.html')
GameSetListView = create_list_view(GameSet, 'gamesets', 'catalog/gamesets.html')
AddressListView = create_list_view(Address, 'addresses', 'catalog/addresses.html')
GenreListView = create_list_view(Genre, 'genres', 'catalog/genres.html')

def create_view(model_class, context_name, template):
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})
    return view

сlub_view = create_view(Club, 'club', 'entities/club.html')
boardgame_view = create_view(BoardGame, 'boardgame', 'entities/boardgame.html')
gameset_view = create_view(GameSet, 'gameset', 'entities/gameset.html')
address_view = create_view(Address, 'address', 'entities/addresses.html')
genre_view = create_view(Genre, 'genre', 'entities/genres.html')

class MyPermission(BasePermission):
    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = 'POST', 'PUT', 'DELETE'

    def has_permission(self, request, _):
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False

def create_viewset(model_class, serializer):
    class CustomViewSet(ModelViewSet):
        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return CustomViewSet

ClubViewSet = create_viewset(Club, ClubSerializer)
BoardGameViewSet = create_viewset(BoardGame, BoardGameSerializer)
GameSetViewSet = create_viewset(GameSet, GameSetSerializer)
GenreViewSet = create_viewset(Genre, GenreSerializer)
AddressViewSet = create_viewset(Address, AddressSerializer)