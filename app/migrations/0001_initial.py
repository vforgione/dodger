# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supplier'
        db.create_table(u'app_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['Supplier'])

        # Adding model 'Category'
        db.create_table(u'app_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['Category'])

        # Adding model 'Brand'
        db.create_table(u'app_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['Brand'])

        # Adding model 'Attribute'
        db.create_table(u'app_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['Attribute'])

        # Adding model 'Sku'
        db.create_table(u'app_sku', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Brand'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reorder_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('notify_at_threshold', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('mfr_sku', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('case_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('qty_on_hand', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Sku'])

        # Adding M2M table for field categories on 'Sku'
        m2m_table_name = db.shorten_name(u'app_sku_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sku', models.ForeignKey(orm[u'app.sku'], null=False)),
            ('category', models.ForeignKey(orm[u'app.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sku_id', 'category_id'])

        # Adding model 'SkuAttribute'
        db.create_table(u'app_skuattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Attribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'app', ['SkuAttribute'])

        # Adding model 'QuantityAdjustmentReason'
        db.create_table(u'app_quantityadjustmentreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['QuantityAdjustmentReason'])

        # Adding model 'SkuQuantityAdjustment'
        db.create_table(u'app_skuquantityadjustment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
            ('new', self.gf('django.db.models.fields.IntegerField')()),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.QuantityAdjustmentReason'])),
            ('detail', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['SkuQuantityAdjustment'])

        # Adding model 'ContactLabel'
        db.create_table(u'app_contactlabel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'app', ['ContactLabel'])

        # Adding model 'Contact'
        db.create_table(u'app_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(default=u'United States', max_length=255)),
            ('represents', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.ContactLabel'])),
        ))
        db.send_create_signal(u'app', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['name', 'represents']
        db.create_unique(u'app_contact', ['name', 'represents_id'])

        # Adding model 'Receiver'
        db.create_table(u'app_receiver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(default=u'United States', max_length=255)),
        ))
        db.send_create_signal(u'app', ['Receiver'])

        # Adding model 'PurchaseOrder'
        db.create_table(u'app_purchaseorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Contact'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Receiver'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['PurchaseOrder'])

        # Adding model 'PurchaseOrderLineItem'
        db.create_table(u'app_purchaseorderlineitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchase_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.PurchaseOrder'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('disc_dollar', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('disc_percent', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('qty_ordered', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'app', ['PurchaseOrderLineItem'])

        # Adding model 'Shipment'
        db.create_table(u'app_shipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('puchase_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.PurchaseOrder'])),
            ('received_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('received_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Shipment'])

        # Adding model 'ShipmentLineItem'
        db.create_table(u'app_shipmentlineitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Shipment'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('qty_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'app', ['ShipmentLineItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Contact', fields ['name', 'represents']
        db.delete_unique(u'app_contact', ['name', 'represents_id'])

        # Deleting model 'Supplier'
        db.delete_table(u'app_supplier')

        # Deleting model 'Category'
        db.delete_table(u'app_category')

        # Deleting model 'Brand'
        db.delete_table(u'app_brand')

        # Deleting model 'Attribute'
        db.delete_table(u'app_attribute')

        # Deleting model 'Sku'
        db.delete_table(u'app_sku')

        # Removing M2M table for field categories on 'Sku'
        db.delete_table(db.shorten_name(u'app_sku_categories'))

        # Deleting model 'SkuAttribute'
        db.delete_table(u'app_skuattribute')

        # Deleting model 'QuantityAdjustmentReason'
        db.delete_table(u'app_quantityadjustmentreason')

        # Deleting model 'SkuQuantityAdjustment'
        db.delete_table(u'app_skuquantityadjustment')

        # Deleting model 'ContactLabel'
        db.delete_table(u'app_contactlabel')

        # Deleting model 'Contact'
        db.delete_table(u'app_contact')

        # Deleting model 'Receiver'
        db.delete_table(u'app_receiver')

        # Deleting model 'PurchaseOrder'
        db.delete_table(u'app_purchaseorder')

        # Deleting model 'PurchaseOrderLineItem'
        db.delete_table(u'app_purchaseorderlineitem')

        # Deleting model 'Shipment'
        db.delete_table(u'app_shipment')

        # Deleting model 'ShipmentLineItem'
        db.delete_table(u'app_shipmentlineitem')


    models = {
        u'app.attribute': {
            'Meta': {'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.contact': {
            'Meta': {'unique_together': "((u'name', u'represents'),)", 'object_name': 'Contact'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.ContactLabel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'represents': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app.contactlabel': {
            'Meta': {'object_name': 'ContactLabel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.purchaseorder': {
            'Meta': {'object_name': 'PurchaseOrder'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Receiver']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"})
        },
        u'app.purchaseorderlineitem': {
            'Meta': {'object_name': 'PurchaseOrderLineItem'},
            'disc_dollar': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'disc_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"}),
            'qty_ordered': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"})
        },
        u'app.quantityadjustmentreason': {
            'Meta': {'object_name': 'QuantityAdjustmentReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.receiver': {
            'Meta': {'object_name': 'Receiver'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app.shipment': {
            'Meta': {'object_name': 'Shipment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'puchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"}),
            'received_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'app.shipmentlineitem': {
            'Meta': {'object_name': 'ShipmentLineItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qty_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Shipment']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"})
        },
        u'app.sku': {
            'Meta': {'object_name': 'Sku'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Brand']"}),
            'case_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Category']", 'symmetrical': 'False'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mfr_sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notify_at_threshold': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'qty_on_hand': ('django.db.models.fields.IntegerField', [], {}),
            'reorder_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"})
        },
        u'app.skuattribute': {
            'Meta': {'object_name': 'SkuAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app.skuquantityadjustment': {
            'Meta': {'object_name': 'SkuQuantityAdjustment'},
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.IntegerField', [], {}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.QuantityAdjustmentReason']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.supplier': {
            'Meta': {'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']