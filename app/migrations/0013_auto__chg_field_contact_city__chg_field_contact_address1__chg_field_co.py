# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Contact.city'
        db.alter_column(u'app_contact', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Contact.address1'
        db.alter_column(u'app_contact', 'address1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Contact.zipcode'
        db.alter_column(u'app_contact', 'zipcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Contact.state'
        db.alter_column(u'app_contact', 'state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Contact.country'
        db.alter_column(u'app_contact', 'country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Receiver.city'
        db.alter_column(u'app_receiver', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Receiver.address1'
        db.alter_column(u'app_receiver', 'address1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Receiver.zipcode'
        db.alter_column(u'app_receiver', 'zipcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Receiver.state'
        db.alter_column(u'app_receiver', 'state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Receiver.country'
        db.alter_column(u'app_receiver', 'country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Contact.city'
        db.alter_column(u'app_contact', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Contact.address1'
        db.alter_column(u'app_contact', 'address1', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Contact.zipcode'
        db.alter_column(u'app_contact', 'zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Contact.state'
        db.alter_column(u'app_contact', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Contact.country'
        db.alter_column(u'app_contact', 'country', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Receiver.city'
        db.alter_column(u'app_receiver', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Receiver.address1'
        db.alter_column(u'app_receiver', 'address1', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Receiver.zipcode'
        db.alter_column(u'app_receiver', 'zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Receiver.state'
        db.alter_column(u'app_receiver', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Receiver.country'
        db.alter_column(u'app_receiver', 'country', self.gf('django.db.models.fields.CharField')(max_length=255))

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
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.ContactLabel']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'represents': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'app.contactlabel': {
            'Meta': {'object_name': 'ContactLabel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.costadjustment': {
            'Meta': {'object_name': 'CostAdjustment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.FloatField', [], {}),
            'old': ('django.db.models.fields.FloatField', [], {}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.CostAdjustmentReason']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.costadjustmentreason': {
            'Meta': {'object_name': 'CostAdjustmentReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.purchaseorder': {
            'Meta': {'object_name': 'PurchaseOrder'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Receiver']"}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'shipping_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'terms': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tracking_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'app.purchaseorderlineitem': {
            'Meta': {'object_name': 'PurchaseOrderLineItem'},
            'discount_dollar': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'discount_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"}),
            'quantity_ordered': ('django.db.models.fields.IntegerField', [], {}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'unit_cost': ('django.db.models.fields.FloatField', [], {})
        },
        u'app.quantityadjustment': {
            'Meta': {'object_name': 'QuantityAdjustment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.IntegerField', [], {}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.QuantityAdjustmentReason']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.quantityadjustmentreason': {
            'Meta': {'object_name': 'QuantityAdjustmentReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app.receiver': {
            'Meta': {'object_name': 'Receiver'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'United States'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'app.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.PurchaseOrder']"})
        },
        u'app.shipmentlineitem': {
            'Meta': {'object_name': 'ShipmentLineItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity_received': ('django.db.models.fields.IntegerField', [], {}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Shipment']"}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"})
        },
        u'app.sku': {
            'Meta': {'object_name': 'Sku'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'action_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Brand']"}),
            'case_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Category']", 'symmetrical': 'False'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'in_live_deal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lead_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'minimum_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notify_at_threshold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'quantity_on_hand': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Supplier']"}),
            'supplier_sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'app.skuattribute': {
            'Meta': {'unique_together': "((u'sku', u'attribute'),)", 'object_name': 'SkuAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sku']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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