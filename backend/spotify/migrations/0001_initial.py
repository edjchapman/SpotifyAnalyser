# Generated by Django 5.0.6 on 2024-07-28 23:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Playlist",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("spotify_id", models.CharField(max_length=50)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("public", models.BooleanField(default=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SpotifyToken",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("access_token", models.CharField(max_length=255)),
                ("refresh_token", models.CharField(max_length=255)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("spotify_id", models.CharField(max_length=50)),
                ("name", models.CharField(max_length=255)),
                ("artist", models.CharField(max_length=255)),
                ("album", models.CharField(max_length=255)),
                ("playlist", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="spotify.playlist")),
            ],
            options={
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
    ]
