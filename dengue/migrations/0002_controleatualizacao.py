from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dengue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControleAtualizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_arquivo', models.CharField(max_length=100)),
                ('ultima_atualizacao', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
