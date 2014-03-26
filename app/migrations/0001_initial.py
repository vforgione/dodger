# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attribute'
        db.create_table(u'app_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['Attribute'])

        # Adding model 'Brand'
        db.create_table(u'app_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['Brand'])

        # Adding model 'Category'
        db.create_table(u'app_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['Category'])

        # Adding model 'ContactLabel'
        db.create_table(u'app_contactlabel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['ContactLabel'])

        # Adding model 'CostAdjustmentReason'
        db.create_table(u'app_costadjustmentreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['CostAdjustmentReason'])

        # Adding model 'QuantityAdjustmentReason'
        db.create_table(u'app_quantityadjustmentreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['QuantityAdjustmentReason'])

        # Adding model 'Supplier'
        db.create_table(u'app_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['Supplier'])

        # Adding model 'Sku'
        db.create_table(u'app_sku', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('upc', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_index=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Brand'])),
            ('quantity_on_hand', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('location', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_index=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
            ('lead_time', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('minimum_quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notify_at_threshold', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('supplier_sku', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('case_quantity', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('in_live_deal', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_subscription', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_index=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_index=True, blank=True)),
            ('action_date', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
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
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'app', ['SkuAttribute'])

        # Adding unique constraint on 'SkuAttribute', fields ['sku', 'attribute']
        db.create_unique(u'app_skuattribute', ['sku_id', 'attribute_id'])

        # Adding model 'CostAdjustment'
        db.create_table(u'app_costadjustment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('old', self.gf('django.db.models.fields.FloatField')()),
            ('new', self.gf('django.db.models.fields.FloatField')()),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CostAdjustmentReason'])),
            ('detail', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['CostAdjustment'])

        # Adding model 'QuantityAdjustment'
        db.create_table(u'app_quantityadjustment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
            ('new', self.gf('django.db.models.fields.IntegerField')()),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.QuantityAdjustmentReason'])),
            ('detail', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['QuantityAdjustment'])

        # Adding model 'Contact'
        db.create_table(u'app_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('address3', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default=u'United States', max_length=255, null=True, blank=True)),
            ('represents', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
        ))
        db.send_create_signal(u'app', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['name', 'represents']
        db.create_unique(u'app_contact', ['name', 'represents_id'])

        # Adding M2M table for field label on 'Contact'
        m2m_table_name = db.shorten_name(u'app_contact_label')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm[u'app.contact'], null=False)),
            ('contactlabel', models.ForeignKey(orm[u'app.contactlabel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contact_id', 'contactlabel_id'])

        # Adding model 'Receiver'
        db.create_table(u'app_receiver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('address1', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('address3', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default=u'United States', max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Receiver'])

        # Adding model 'PurchaseOrder'
        db.create_table(u'app_purchaseorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Supplier'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Contact'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Receiver'])),
            ('note', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('terms', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tracking_url', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, null=True, blank=True)),
            ('shipping_cost', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('sales_tax', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'app', ['PurchaseOrder'])

        # Adding model 'PurchaseOrderLineItem'
        db.create_table(u'app_purchaseorderlineitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchase_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.PurchaseOrder'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('quantity_ordered', self.gf('django.db.models.fields.IntegerField')()),
            ('unit_cost', self.gf('django.db.models.fields.FloatField')()),
            ('discount_percent', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('discount_dollar', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['PurchaseOrderLineItem'])

        # Adding model 'Shipment'
        db.create_table(u'app_shipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('purchase_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.PurchaseOrder'])),
            ('note', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Shipment'])

        # Adding model 'ShipmentLineItem'
        db.create_table(u'app_shipmentlineitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Shipment'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Sku'])),
            ('quantity_received', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['ShipmentLineItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Contact', fields ['name', 'represents']
        db.delete_unique(u'app_contact', ['name', 'represents_id'])

        # Removing unique constraint on 'SkuAttribute', fields ['sku', 'attribute']
        db.delete_unique(u'app_skuattribute', ['sku_id', 'attribute_id'])

        # Deleting model 'Attribute'
        db.delete_table(u'app_attribute')

        # Deleting model 'Brand'
        db.delete_table(u'app_brand')

        # Deleting model 'Category'
        db.delete_table(u'app_category')

        # Deleting model 'ContactLabel'
        db.delete_table(u'app_contactlabel')

        # Deleting model 'CostAdjustmentReason'
        db.delete_table(u'app_costadjustmentreason')

        # Deleting model 'QuantityAdjustmentReason'
        db.delete_table(u'app_quantityadjustmentreason')

        # Deleting model 'Supplier'
        db.delete_table(u'app_supplier')

        # Deleting model 'Sku'
        db.delete_table(u'app_sku')

        # Removing M2M table for field categories on 'Sku'
        db.delete_table(db.shorten_name(u'app_sku_categories'))

        # Deleting model 'SkuAttribute'
        db.delete_table(u'app_skuattribute')

        # Deleting model 'CostAdjustment'
        db.delete_table(u'app_costadjustment')

        # Deleting model 'QuantityAdjustment'
        db.delete_table(u'app_quantityadjustment')

        # Deleting model 'Contact'
        db.delete_table(u'app_contact')

        # Removing M2M table for field label on 'Contact'
        db.delete_table(db.shorten_name(u'app_contact_label'))

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
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.brand': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.category': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.contact': {
            'Meta': {'ordering': "(u'name', u'represents')", 'unique_together': "((u'name', u'represents'),)", 'object_name': 'Contact'},
            'address1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.ContactLabel']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'represents': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'app.contactlabel': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'ContactLabel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.costadjustment': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'CostAdjustment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.FloatField', [], {}),
            'old': ('django.db.models.fields.FloatField', [], {}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.CostAdjustmentReason']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.costadjustmentreason': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'CostAdjustmentReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.purchaseorder': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'PurchaseOrder'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Receiver']"}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'shipping_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'terms': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tracking_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'app.purchaseorderlineitem': {
            'Meta': {'ordering': "(u'-purchase_order__id', u'sku__id')", 'object_name': 'PurchaseOrderLineItem'},
            'discount_dollar': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'discount_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"}),
            'quantity_ordered': ('django.db.models.fields.IntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'unit_cost': ('django.db.models.fields.FloatField', [], {})
        },
        u'app.quantityadjustment': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'QuantityAdjustment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.IntegerField', [], {}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.QuantityAdjustmentReason']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.quantityadjustmentreason': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'QuantityAdjustmentReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'app.receiver': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Receiver'},
            'address1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'app.shipment': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'Shipment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"})
        },
        u'app.shipmentlineitem': {
            'Meta': {'ordering': "(u'-shipment__id', u'sku__id')", 'object_name': 'ShipmentLineItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity_received': ('django.db.models.fields.IntegerField', [], {}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Shipment']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"})
        },
        u'app.sku': {
            'Meta': {'ordering': "(u'id',)", 'object_name': 'Sku'},
            'action': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'action_date': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Brand']"}),
            'case_quantity': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Category']", 'symmetrical': 'False'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'in_live_deal': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lead_time': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'minimum_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'notify_at_threshold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'quantity_on_hand': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'supplier_sku': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'app.skuattribute': {
            'Meta': {'ordering': "(u'sku__id', u'attribute__name')", 'unique_together': "((u'sku', u'attribute'),)", 'object_name': 'SkuAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'app.supplier': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
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