# Generated by Django 5.0.3 on 2024-05-14 19:59

import django.db.models.deletion
import main_game.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('region', models.TextField(max_length=100, verbose_name='region')),
                ('sity', models.TextField(blank=True, max_length=100, null=True, verbose_name='sity')),
                ('street', models.TextField(blank=True, max_length=100, null=True, verbose_name='street')),
                ('home', models.TextField(blank=True, max_length=100, null=True, verbose_name='home')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'db_table': '"game_site"."addresses"',
                'ordering': ['region', 'sity', 'street'],
            },
        ),
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('level', models.PositiveIntegerField(validators=[main_game.models.check_level], verbose_name='level')),
            ],
            options={
                'verbose_name': 'board_game',
                'db_table': '"game_site"."board_games"',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('phone_number', models.TextField(validators=[main_game.models.phone_number_validator], verbose_name='phone_number')),
            ],
            options={
                'verbose_name': 'club',
                'db_table': '"game_site"."clubs"',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GameSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('name', models.TextField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'game_set',
                'db_table': '"game_site"."game_sets"',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ClubAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.address', verbose_name='address')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.club', verbose_name='club')),
            ],
            options={
                'verbose_name': 'relationship club address',
                'db_table': '"game_site"."club_address"',
                'unique_together': {('club', 'address')},
            },
        ),
        migrations.AddField(
            model_name='club',
            name='addresses',
            field=models.ManyToManyField(through='main_game.ClubAddress', to='main_game.address'),
        ),
        migrations.AddField(
            model_name='address',
            name='clubs',
            field=models.ManyToManyField(through='main_game.ClubAddress', to='main_game.club'),
        ),
        migrations.CreateModel(
            name='ClubToGame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.club', verbose_name='club')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.boardgame', verbose_name='board_games')),
            ],
            options={
                'verbose_name': 'relationship club game',
                'db_table': '"game_site"."club_to_game"',
                'unique_together': {('club', 'game')},
            },
        ),
        migrations.AddField(
            model_name='club',
            name='games',
            field=models.ManyToManyField(through='main_game.ClubToGame', to='main_game.boardgame'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='clubs',
            field=models.ManyToManyField(through='main_game.ClubToGame', to='main_game.club'),
        ),
        migrations.CreateModel(
            name='GameGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.boardgame', verbose_name='board_games')),
            ],
            options={
                'verbose_name': 'relationship game genre',
                'db_table': '"game_site"."game_genre"',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('name', models.TextField(default='no genre', max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='description')),
                ('games', models.ManyToManyField(through='main_game.GameGenre', to='main_game.boardgame')),
            ],
            options={
                'verbose_name': 'genre',
                'db_table': '"game_site"."genres"',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='gamegenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.genre', verbose_name='genre'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='genres',
            field=models.ManyToManyField(through='main_game.GameGenre', to='main_game.genre'),
        ),
        migrations.CreateModel(
            name='SetToGame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=main_game.models.get_datetime, null=True, validators=[main_game.models.check_modified], verbose_name='modified')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.boardgame', verbose_name='board_games')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_game.gameset', verbose_name='game_set')),
            ],
            options={
                'verbose_name': 'relationship set game',
                'db_table': '"game_site"."set_to_game"',
                'unique_together': {('set', 'game')},
            },
        ),
        migrations.AddField(
            model_name='gameset',
            name='games',
            field=models.ManyToManyField(through='main_game.SetToGame', to='main_game.boardgame'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='sets',
            field=models.ManyToManyField(through='main_game.SetToGame', to='main_game.gameset'),
        ),
        migrations.AlterUniqueTogether(
            name='gamegenre',
            unique_together={('game', 'genre')},
        ),
    ]
