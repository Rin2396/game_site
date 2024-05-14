from django.db import models
from uuid import uuid4
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


NAME_MAX_LEN = 100
ADDRESS_MAX_LEN = 100
PHONE_MAX_LEN = 12
DESCRIPTION_MAX_LEN = 1000


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def get_datetime():
    return datetime.now(timezone.utc)


def check_created(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )


def check_modified(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )


def check_level(number) -> None:
    if number < 0 or number > 100:
        raise ValidationError('value should be greater than zero and less than hundred')


def phone_number_validator(number: str) -> None:
    rule = re.compile(r'^\+7[0-9]{3}[0-9]{7}$')
    if not rule.search(number):
        raise ValidationError(
            _('Number must be in format +79999999999'),
            params={'phone_number': number}
        )



class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_modified]
    )

    class Meta:
        abstract = True



class Club(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False, max_length=ADDRESS_MAX_LEN)
    phone_number = models.TextField(_('phone_number'), null=False, blank=False, validators=[phone_number_validator])

    games = models.ManyToManyField('BoardGame', through='ClubToGame')
    addresses = models.ManyToManyField('Address', through='ClubAddress')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = '"game_site"."clubs"'
        ordering = ['name']
        verbose_name = _('club')


class BoardGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN)
    level = models.PositiveIntegerField(_('level'), null=False, blank=False, validators=[check_level])

    genres = models.ManyToManyField('Genre', through='GameGenre')
    clubs = models.ManyToManyField('Club', through='ClubToGame')
    sets = models.ManyToManyField('GameSet', through='SetToGame')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"game_site"."board_games"'
        ordering = ['name']
        verbose_name = _('board_game')


class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN, default='no genre')
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LEN)

    games = models.ManyToManyField('BoardGame', through='GameGenre')

    def __str__(self) -> str:
        return f'{self.name}: {self.description}'
    
    class Meta:
        db_table = '"game_site"."genres"'
        ordering = ['name']
        verbose_name = _('genre')


class Address(UUIDMixin, CreatedMixin, ModifiedMixin):
    region = models.TextField(_('region'), null=False, blank=False, max_length=NAME_MAX_LEN)
    sity = models.TextField(_('sity'), null=False, blank=True, default='Sirius', max_length=NAME_MAX_LEN)
    street = models.TextField(_('street'), null=True, blank=True, max_length=NAME_MAX_LEN)
    home = models.TextField(_('home'), null=True, blank=True, max_length=NAME_MAX_LEN)

    clubs = models.ManyToManyField('Club', through='ClubAddress')

    def __str__(self) -> str:
        return f'{self.region}, {self.sity}, {self.street}, {self.home}'

    class Meta:
        db_table = '"game_site"."addresses"'
        ordering = ['region', 'sity', 'street']
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class GameSet(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN)
    description = models.TextField(_('description'), null=False, blank=True, default='', max_length=DESCRIPTION_MAX_LEN)

    games = models.ManyToManyField('BoardGame', through='SetToGame')

    def __str__(self) -> str:
        return f'{self.name}: {self.description}'

    class Meta:
        db_table = '"game_site"."game_sets"'
        ordering = ['name']
        verbose_name = _('game_set')


class ClubToGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    club = models.ForeignKey(Club, verbose_name=_('club'), on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, verbose_name=_('board_games'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"club {self.club} - game {self.game}"

    class Meta:
        db_table = '"game_site"."club_to_game"'
        unique_together = (
            ('club', 'game'),
        )
        verbose_name = _('relationship club game')


class SetToGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    set = models.ForeignKey(GameSet, verbose_name=_('game_set'), on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, verbose_name=_('board_games'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"set {self.set} - game {self.game}"

    class Meta:
        db_table = '"game_site"."set_to_game"'
        unique_together = (
            ('set', 'game'),
        )
        verbose_name = _('relationship set game')


class GameGenre(UUIDMixin, CreatedMixin, ModifiedMixin):
    game = models.ForeignKey(BoardGame, verbose_name=_('board_games'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"game {self.game} - genre {self.genre}"

    class Meta:
        db_table = '"game_site"."game_genre"'
        unique_together = (
            ('game', 'genre'),
        )
        verbose_name = _('relationship game genre')


class ClubAddress(UUIDMixin, CreatedMixin, ModifiedMixin):
    club = models.ForeignKey(Club, verbose_name=_('club'), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name=_('address'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"club {self.club} - address {self.address}"

    class Meta:
        db_table = '"game_site"."club_address"'
        unique_together = (
            ('club', 'address'),
        )
        verbose_name = _('relationship club address')
