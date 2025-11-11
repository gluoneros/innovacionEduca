# Generated manually for adding updated_at field to Materia model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0005_remove_grado_periodo_grado_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]