# Generated by Django 2.1.4 on 2019-03-26 06:10

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product Attribute',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='AttributeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('delete_dt', models.DateTimeField(blank=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Attribute')),
            ],
            options={
                'verbose_name': 'Product Attribute Item',
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='BasketWishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(blank=True, max_length=32, null=True)),
                ('basket_flag', models.BooleanField(default=True)),
                ('quantity', models.IntegerField(default=1)),
                ('weight', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('visible_code', models.CharField(max_length=14, unique=True)),
                ('payment_method', models.CharField(max_length=12)),
                ('status', models.IntegerField(choices=[(10, 'New: pending send to gateway'), (20, 'Pending: Awaiting gateway response'), (30, 'Success: pending POST to Salebox'), (31, 'Success: successfully POSTed to Salebox'), (40, 'Rejected: gateway rejected payment'), (50, 'Timeout: gateway did not respond in an acceptable time period')])),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutStoreUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(10, 'New: pending send to gateway'), (20, 'Pending: Awaiting gateway response'), (30, 'Success: pending POST to Salebox'), (31, 'Success: successfully POSTed to Salebox'), (40, 'Rejected: gateway rejected payment'), (50, 'Timeout: gateway did not respond in an acceptable time period')])),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.CheckoutStore')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_2', models.CharField(blank=True, max_length=2, null=True)),
                ('code_3', models.CharField(blank=True, max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('default', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CountryState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_2', models.CharField(blank=True, max_length=2, null=True)),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Country')),
            ],
            options={
                'verbose_name_plural': 'Country States',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CountryStateTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=7)),
                ('value', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.CountryState')),
            ],
            options={
                'verbose_name': 'Country State Translations',
                'ordering': ['language', 'state'],
            },
        ),
        migrations.CreateModel(
            name='CountryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=7)),
                ('value', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Country')),
            ],
            options={
                'verbose_name': 'Country Translations',
                'ordering': ['language', 'country'],
            },
        ),
        migrations.CreateModel(
            name='DiscountGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('group_type', models.CharField(choices=[('S', 'Seasonal'), ('M', 'Manual')], default='M', max_length=1)),
                ('operational_flag', models.BooleanField(default=False)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Discount Group',
            },
        ),
        migrations.CreateModel(
            name='DiscountRuleset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('discount_type', models.CharField(choices=[('flat_percent', 'Flat Percentage')], default='flat_percent', max_length=12)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('start_dt', models.DateTimeField(blank=True, null=True)),
                ('end_dt', models.DateTimeField(blank=True, null=True)),
                ('operational_flag', models.BooleanField(default=True)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.DiscountGroup')),
            ],
            options={
                'verbose_name': 'Discount Ruleset',
            },
        ),
        migrations.CreateModel(
            name='LastUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=36)),
                ('value', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'Last Update',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, max_length=25)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unspecified')], max_length=1, null=True)),
                ('title', models.IntegerField(blank=True, choices=[(1, 'Mr'), (2, 'Mrs'), (3, 'Miss')], null=True)),
                ('name_first', models.CharField(blank=True, max_length=20, null=True)),
                ('name_last', models.CharField(blank=True, max_length=30, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address_1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('address_3', models.CharField(blank=True, max_length=255, null=True)),
                ('address_4', models.CharField(blank=True, max_length=255, null=True)),
                ('address_5', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=12, null=True)),
                ('phone_1', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_2', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('id_card', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('R', 'Resigned'), ('S', 'Suspended'), ('T', 'Terminated')], default='A', max_length=1)),
                ('active_flag', models.BooleanField(default=True)),
                ('join_date', models.DateField(blank=True, null=True)),
                ('string_1', models.CharField(blank=True, max_length=255, null=True)),
                ('string_2', models.CharField(blank=True, max_length=255, null=True)),
                ('string_3', models.CharField(blank=True, max_length=255, null=True)),
                ('string_4', models.CharField(blank=True, max_length=255, null=True)),
                ('string_5', models.CharField(blank=True, max_length=255, null=True)),
                ('string_6', models.CharField(blank=True, max_length=255, null=True)),
                ('string_7', models.CharField(blank=True, max_length=255, null=True)),
                ('string_8', models.CharField(blank=True, max_length=255, null=True)),
                ('string_9', models.CharField(blank=True, max_length=255, null=True)),
                ('string_10', models.CharField(blank=True, max_length=255, null=True)),
                ('string_11', models.CharField(blank=True, max_length=255, null=True)),
                ('string_12', models.CharField(blank=True, max_length=255, null=True)),
                ('string_13', models.CharField(blank=True, max_length=255, null=True)),
                ('string_14', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Country')),
                ('country_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.CountryState')),
            ],
            options={
                'verbose_name': 'Member',
                'ordering': ['guid'],
            },
        ),
        migrations.CreateModel(
            name='MemberGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('flat_discount_percentage', models.FloatField(default=0)),
                ('can_be_parent', models.BooleanField(default=True)),
                ('default_group', models.BooleanField(default=False)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Member Group',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('string_1', models.CharField(blank=True, max_length=150, null=True)),
                ('string_2', models.CharField(blank=True, max_length=150, null=True)),
                ('string_3', models.CharField(blank=True, max_length=150, null=True)),
                ('string_4', models.CharField(blank=True, max_length=150, null=True)),
                ('sold_by', models.CharField(choices=[('item', 'item'), ('weight', 'weight')], default='item', max_length=6)),
                ('vat_applicable', models.BooleanField(default=True)),
                ('image', models.CharField(blank=True, max_length=70, null=True)),
                ('local_image', models.CharField(blank=True, max_length=25, null=True)),
                ('inventory_flag', models.BooleanField(default=True)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('bestseller_rank', models.IntegerField(default=0)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('rating_score', models.IntegerField(default=0)),
                ('rating_vote_count', models.IntegerField(default=0)),
                ('attribute_1', models.ManyToManyField(blank=True, related_name='product_attr_1', to='saleboxdjango.AttributeItem')),
                ('attribute_10', models.ManyToManyField(blank=True, related_name='product_attr_10', to='saleboxdjango.AttributeItem')),
                ('attribute_2', models.ManyToManyField(blank=True, related_name='product_attr_2', to='saleboxdjango.AttributeItem')),
                ('attribute_3', models.ManyToManyField(blank=True, related_name='product_attr_3', to='saleboxdjango.AttributeItem')),
                ('attribute_4', models.ManyToManyField(blank=True, related_name='product_attr_4', to='saleboxdjango.AttributeItem')),
                ('attribute_5', models.ManyToManyField(blank=True, related_name='product_attr_5', to='saleboxdjango.AttributeItem')),
                ('attribute_6', models.ManyToManyField(blank=True, related_name='product_attr_6', to='saleboxdjango.AttributeItem')),
                ('attribute_7', models.ManyToManyField(blank=True, related_name='product_attr_7', to='saleboxdjango.AttributeItem')),
                ('attribute_8', models.ManyToManyField(blank=True, related_name='product_attr_8', to='saleboxdjango.AttributeItem')),
                ('attribute_9', models.ManyToManyField(blank=True, related_name='product_attr_9', to='saleboxdjango.AttributeItem')),
            ],
            options={
                'verbose_name': 'Product',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(blank=True, max_length=70, null=True)),
                ('local_image', models.CharField(blank=True, max_length=25, null=True)),
                ('seasonal_flag', models.BooleanField(default=False)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('slug_path', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='saleboxdjango.ProductCategory')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=150)),
                ('bo_name', models.CharField(blank=True, default='', max_length=200)),
                ('plu', models.CharField(blank=True, default='', max_length=25)),
                ('sku', models.CharField(blank=True, default='', max_length=25)),
                ('color', models.CharField(blank=True, default='', max_length=50)),
                ('size', models.CharField(blank=True, default='', max_length=20)),
                ('size_order', models.FloatField(default=0)),
                ('size_uom', models.CharField(blank=True, choices=[('', 'n/a'), ('g', 'g'), ('kg', 'kg'), ('ml', 'ml')], default='', max_length=2)),
                ('price', models.IntegerField(null=True)),
                ('sale_price', models.IntegerField(default=0)),
                ('sale_percent', models.IntegerField(default=0)),
                ('barcode', models.CharField(blank=True, default='', max_length=50)),
                ('available_to_order', models.BooleanField(default=True)),
                ('available_on_pos', models.BooleanField(default=True)),
                ('available_on_ecom', models.BooleanField(default=True)),
                ('shelf_expiry_type', models.CharField(default='manual', max_length=12)),
                ('shelf_life_days', models.IntegerField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=150, null=True)),
                ('image', models.CharField(blank=True, max_length=70, null=True)),
                ('local_image', models.CharField(blank=True, max_length=20, null=True)),
                ('unique_string', models.CharField(blank=True, max_length=255)),
                ('shipping_weight', models.IntegerField(blank=True, null=True)),
                ('loyalty_points', models.FloatField(blank=True, null=True)),
                ('member_discount_applicable', models.BooleanField(default=True)),
                ('string_1', models.CharField(blank=True, max_length=150, null=True)),
                ('string_2', models.CharField(blank=True, max_length=150, null=True)),
                ('string_3', models.CharField(blank=True, max_length=150, null=True)),
                ('string_4', models.CharField(blank=True, max_length=150, null=True)),
                ('warehouse_location', models.CharField(blank=True, max_length=50, null=True)),
                ('int_1', models.IntegerField(blank=True, null=True)),
                ('int_2', models.IntegerField(blank=True, null=True)),
                ('int_3', models.IntegerField(blank=True, null=True)),
                ('int_4', models.IntegerField(blank=True, null=True)),
                ('date_1', models.DateField(blank=True, null=True)),
                ('date_2', models.DateField(blank=True, null=True)),
                ('active_flag', models.BooleanField(default=True)),
                ('ecommerce_description', models.TextField(blank=True, null=True)),
                ('bestseller_rank', models.IntegerField(default=0)),
                ('default_image', models.CharField(blank=True, max_length=35, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('rating_score', models.IntegerField(default=0)),
                ('rating_vote_count', models.IntegerField(default=0)),
                ('name_sorted', models.IntegerField(db_index=True, default=0)),
                ('attribute_1', models.ManyToManyField(blank=True, related_name='variant_attr_1', to='saleboxdjango.AttributeItem')),
                ('attribute_10', models.ManyToManyField(blank=True, related_name='variant_attr_10', to='saleboxdjango.AttributeItem')),
                ('attribute_2', models.ManyToManyField(blank=True, related_name='variant_attr_2', to='saleboxdjango.AttributeItem')),
                ('attribute_3', models.ManyToManyField(blank=True, related_name='variant_attr_3', to='saleboxdjango.AttributeItem')),
                ('attribute_4', models.ManyToManyField(blank=True, related_name='variant_attr_4', to='saleboxdjango.AttributeItem')),
                ('attribute_5', models.ManyToManyField(blank=True, related_name='variant_attr_5', to='saleboxdjango.AttributeItem')),
                ('attribute_6', models.ManyToManyField(blank=True, related_name='variant_attr_6', to='saleboxdjango.AttributeItem')),
                ('attribute_7', models.ManyToManyField(blank=True, related_name='variant_attr_7', to='saleboxdjango.AttributeItem')),
                ('attribute_8', models.ManyToManyField(blank=True, related_name='variant_attr_8', to='saleboxdjango.AttributeItem')),
                ('attribute_9', models.ManyToManyField(blank=True, related_name='variant_attr_9', to='saleboxdjango.AttributeItem')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Product')),
            ],
            options={
                'verbose_name': 'Product Variant',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductVariantImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(default='', max_length=100)),
                ('local_img', models.CharField(blank=True, max_length=25, null=True)),
                ('img_height', models.IntegerField(default=0)),
                ('img_width', models.IntegerField(default=0)),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('active_flag', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.ProductVariant')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ProductVariantRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.ProductVariant')),
            ],
            options={
                'verbose_name': 'Product Variant Rating',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.BooleanField(default=False)),
                ('address_group', models.CharField(default='default', max_length=10)),
                ('full_name', models.CharField(max_length=150)),
                ('address_1', models.CharField(max_length=150)),
                ('address_2', models.CharField(blank=True, max_length=150, null=True)),
                ('address_3', models.CharField(blank=True, max_length=150, null=True)),
                ('address_4', models.CharField(blank=True, max_length=150, null=True)),
                ('address_5', models.CharField(blank=True, max_length=150, null=True)),
                ('postcode', models.CharField(blank=True, max_length=12, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Country')),
                ('country_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.CountryState')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Address',
                'ordering': ['-default', 'full_name', 'address_1'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.ProductCategory'),
        ),
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.MemberGroup'),
        ),
        migrations.AddField(
            model_name='member',
            name='group_when_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_when_created', to='saleboxdjango.MemberGroup'),
        ),
        migrations.AddField(
            model_name='member',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.Member'),
        ),
        migrations.AddField(
            model_name='discountruleset',
            name='product_variant',
            field=models.ManyToManyField(blank=True, to='saleboxdjango.ProductVariant'),
        ),
        migrations.AddField(
            model_name='basketwishlist',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saleboxdjango.ProductVariant'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['bestseller_rank', 'name_sorted'], name='saleboxdjan_bestsel_5ad3e6_idx'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['-bestseller_rank', 'name_sorted'], name='saleboxdjan_bestsel_e36854_idx'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['sale_price', 'name_sorted'], name='saleboxdjan_sale_pr_1681f7_idx'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['-sale_price', 'name_sorted'], name='saleboxdjan_sale_pr_90497c_idx'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['rating_score', 'name_sorted'], name='saleboxdjan_rating__c1dad4_idx'),
        ),
        migrations.AddIndex(
            model_name='productvariant',
            index=models.Index(fields=['-rating_score', 'name_sorted'], name='saleboxdjan_rating__4d1500_idx'),
        ),
    ]
