# Generated by Django 4.2.3 on 2023-08-17 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_wallet_wallettransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='message',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking_no',
        ),
        migrations.AddField(
            model_name='order',
            name='address_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='cancelled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('CANCELLED', 'Cancelled'), ('DELIVERED', 'Delivered'), ('SHIPPED', 'Shipped'), ('RETURNED', 'Returned'), ('REQUESTED FOR RETURN', 'Requested for return'), ('ORDERED', 'Ordered')], default='Ordered', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='return_period_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('PREPAID', 'PREPAID'), ('CASH_ON_DELIVERY', 'Cash on Delivery'), ('WALLET', 'wallet')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled'), ('DELIVERED', 'Delivered'), ('SHIPPED', 'shipped'), ('ORDERED', 'ordered'), ('RETURN', 'return'), ('REFUND', 'refund')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_required', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('comment', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]