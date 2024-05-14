from typing import Any
from django.contrib import admin
from .models import Club, BoardGame, ClubToGame, GameSet, Genre, Address, ClubAddress, GameGenre, SetToGame
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class ClubToGameInline(admin.TabularInline):
    model = ClubToGame
    extra = 1

class SetToGameInline(admin.TabularInline):
    model = SetToGame
    extra = 1

class GameGenreInline(admin.TabularInline):
    model = GameGenre
    extra = 1

class ClubAddressInline(admin.TabularInline):
    model = ClubAddress
    extra = 1


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    model = BoardGame
    search_fields = ['name', 'genre', 'level']
    inlines = (ClubToGameInline, SetToGameInline, GameGenreInline)

@admin.register(GameSet)
class GameSetAdmin(admin.ModelAdmin):
    model = GameSet
    search_fields = ['name']
    inlines = (SetToGameInline,)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    model = Club
    search_fields = ['name', 'address', 'phone_number']
    inlines = (ClubToGameInline,)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    inlines = (ClubAddressInline,)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = (GameGenreInline,)