# Generated by Django 2.0.3 on 2018-03-30 18:00

import _socket
from django.conf import settings
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_revision.revision_field
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_model_fields.fields.uuid_auto_field
import edc_utils


class Migration(migrations.Migration):

    replaces = [
        ("edc_identifier", "0001_initial"),
        ("edc_identifier", "0002_auto_20160505_1435"),
        ("edc_identifier", "0003_auto_20160625_0938"),
        ("edc_identifier", "0004_auto_20160807_1443"),
        (
            "edc_identifier",
            "0005_historicalidentifierhistory_historicalidentifiertracker_historicalsubjectidentifier",
        ),
        ("edc_identifier", "0006_auto_20161127_2226"),
        ("edc_identifier", "0007_auto_20161204_2227"),
        ("edc_identifier", "0008_identifiermodel_linked_identifier"),
        ("edc_identifier", "0009_auto_20161221_2323"),
        ("edc_identifier", "0010_auto_20170112_0602"),
        ("edc_identifier", "0011_auto_20170511_1323"),
        ("edc_identifier", "0012_auto_20171116_1606"),
        ("edc_identifier", "0013_auto_20171230_1316"),
        ("edc_identifier", "0014_auto_20180103_1322"),
        ("edc_identifier", "0015_auto_20180116_1235"),
        ("edc_identifier", "0016_auto_20180116_1411"),
        ("edc_identifier", "0017_identifiermodel_subject_identifier"),
        ("edc_identifier", "0018_auto_20180128_1054"),
    ]

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="IdentifierModel",
            fields=[
                (
                    "created",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "id",
                    edc_model_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("sequence_number", models.IntegerField()),
                ("identifier", models.CharField(max_length=50, unique=True)),
                ("device_id", models.IntegerField(default=99)),
                ("protocol_number", models.CharField(max_length=3)),
                ("model", models.CharField(max_length=50, null=True)),
                ("subject_type", models.CharField(max_length=25, null=True)),
                ("study_site", models.CharField(max_length=25)),
                ("linked_identifier", models.CharField(max_length=50, null=True)),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
            ],
            options={"ordering": ["sequence_number"]},
        ),
        migrations.AlterUniqueTogether(
            name="identifiermodel", unique_together={("name", "identifier")}
        ),
        migrations.AlterModelManagers(
            name="identifiermodel",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.RenameField(
            model_name="identifiermodel",
            old_name="subject_type",
            new_name="identifier_type",
        ),
        migrations.RemoveField(model_name="identifiermodel", name="study_site"),
        migrations.AddField(
            model_name="identifiermodel",
            name="identifier_prefix",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name="identifiermodel",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sites.Site",
            ),
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="sequence_number",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="identifiermodel", name="device_id", field=models.IntegerField()
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="identifier_type",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="model",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="protocol_number",
            field=models.CharField(max_length=25),
        ),
        migrations.AlterModelManagers(name="identifiermodel", managers=[]),
        migrations.AlterField(
            model_name="identifiermodel",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="sites.Site",
            ),
        ),
        migrations.AddField(
            model_name="identifiermodel",
            name="subject_identifier",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="identifiermodel",
            name="protocol_number",
            field=models.CharField(max_length=25, null=True),
        ),
    ]
