# Generated by Django 4.1.9 on 2023-05-25 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0007_estudiante_aumento_1_estudiante_aumento_2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaccion',
            old_name='info_factura_dependencia',
            new_name='informacion_transaccion',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='descripcion',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaccion',
            name='estado_transaccion',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('pagada', 'Pagada'), ('abonado', 'Abonado')], default='pendiente', max_length=10),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='hora_transaccion',
            field=models.TimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaccion',
            name='valor_transaccion',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_recibidas', to='Usuarios.estudiante'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='fecha_transaccion',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='fecha_vencimiento_transaccion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='financiera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_creadas', to='Usuarios.financiera'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='monto_transaccion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='origen',
            field=models.CharField(choices=[('transaccion', 'Transacción'), ('estudiante', 'Estudiante')], default='transaccion', max_length=12),
        ),
    ]
