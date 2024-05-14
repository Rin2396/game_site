from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Club, BoardGame, GameSet, Genre, Address

class ClubSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id', 'name',
            'phone_number', 'games', 'addresses',
        ]

class BoardGameSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = BoardGame
        fields = [
            'id', 'name', 'genres',
            'level', 'clubs',
        ]

class GameSetSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = GameSet
        fields = [
            'id', 'name', 'description', 'games',
        ]

class GenreSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id', 'name', 'description', 'games',
        ]

class AddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'region', 'sity',
            'street', 'home', 'clubs',
        ]