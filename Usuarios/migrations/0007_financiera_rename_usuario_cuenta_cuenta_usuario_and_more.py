# Generated by Django 4.1.9 on 2023-05-14 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0006_remove_estudiante_fecha_a_pagar_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Financiera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_financiera', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ultima_actualizacion_financiera', models.DateTimeField(auto_now=True)),
                ('fecha_limite_pago_1', models.DateField(blank=True, null=True)),
                ('fecha_limite_pago_2', models.DateField(blank=True, null=True)),
                ('fecha_limite_pago_3', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Financiera',
                'verbose_name_plural': 'Financieras',
            },
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='usuario_cuenta',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='amigos_usuario',
            new_name='amigos',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='apellidos_usuario',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='email_usuario',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='foto_perfil_usuario',
            new_name='foto_perfil',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='identificacion_usuario',
            new_name='identificacion',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='nombres_usuario',
            new_name='nombres',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='dependencia_origen',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='usuario_destino',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='usuario_origen',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_enviadas', to='Usuarios.usuario'),
        ),
        migrations.DeleteModel(
            name='Dependencia',
        ),
        migrations.AddField(
            model_name='financiera',
            name='usuarios_financiera',
            field=models.ManyToManyField(blank=True, related_name='financieras', to='Usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='financiera_destino',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_recibidas', to='Usuarios.financiera'),
        ),
    ]
