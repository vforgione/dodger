$(document).ready(function(){
  // global scope options
  var options = '<option></option>';

  // listen for change in po selection
  $('select#purchase-order').change(function(){

      // get details on po
      $.ajax({
        url: '/api/dat/purchase-orders/' + $(this).val() + '/',
        type: 'GET',
        dataType: 'json',
        async: false,  // make blocking call
        success: function(xhr, status){
          // set supplier to retrieve products
          var supplier_uri = xhr.supplier;
          $.ajax({
            url: supplier_uri,
            type: 'GET',
            dataType: 'json',
            async: false,  // make blocking call
            success: function(xhr, status){ $('input#supplier').val(xhr.id); },
            error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
            beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
          });
        },
        error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
      });

      // load up products from supplier - the rationale is that the supplier could screw up and switch skus
      $.ajax({
        url: '/api/inventory-manager/products/?supplier__id=' + $('input#supplier').val(),
        type: 'GET',
        dataType: 'json',
        success: function(xhr, status){
          $(xhr.objects).each(function(i){
            options += '<option value="' + xhr.objects[i].sku + '">' + xhr.objects[i].description  + '</option>';
          });
        },
        error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); },
        complete: function(){ $('select.product').html(options); }
      });

      // get order products info for info pane
      $.ajax({
        url: '/api/dat/purchase-order-products/?purchase_order__id=' + $(this).val(),
        type: 'GET',
        dataType: 'json',
        success: function(xhr, status){
          var products = '<p>&nbsp;</p><h3>Order Details</h3><table class="table table-striped"><thead><tr><th>Product</th><th>Qty Ordered</th>';
          $(xhr.objects).each(function(i){
            $.ajax({
              url: xhr.objects[i].product,
              type: 'GET',
              dataType: 'json',
              async: false,
              success: function(xhr, status){ products += '<tr><td>' + xhr.description + '</td>'; },
              error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
              beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
            });
            products += '<td>' + xhr.objects[i].qty_ordered + '</td></tr>';
          });
          products += '</tbody></table>';
          $('#order-info').html(products);
        },
        error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
      });

  });

});
