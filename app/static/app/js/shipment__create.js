$(document).ready(function(){
  // global scope options
  var options = '<option></option>';

  // listen for change in po selection
  $('#id_purchase_order').change(function(){

      // get details on po
      $.ajax({
        url: '/api/sku-service/purchase-orders/' + $(this).val() + '/',
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
            success: function(xhr, status){ $('#supplier').val(xhr.id); },
            error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
            beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034'); }
          });
        },
        error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034'); }
      });

      // load up sku from supplier - the rationale is that the supplier could screw up and switch skus
      $.ajax({
        url: '/api/sku-service/skus/?supplier__id=' + $('#supplier').val(),
        type: 'GET',
        dataType: 'json',
        success: function(xhr, status){
          $(xhr.objects).each(function(i){
            options += '<option value="' + xhr.objects[i].id + '">' + xhr.objects[i].description  + '</option>';
          });
        },
        error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034'); },
        complete: function(){ $('.sku').html(options); }
      });


      // load up info pane
      $.ajax({
        url: "/api/sku-service/purchase-order-line-items/?purchase_order__id=" + $(this).val(),
        type: "GET",
        dataType: "json",
        success: function(xhr){
          var info = '<h4>PO Detail</h4><table class="table table-condensed"><thead><tr><th>SKU</th><th>Qty Ordered</th></tr></thead><tbody>';
          $(xhr.objects).each(function(i){
            $.ajax({
              url: xhr.objects[i].sku,
              type: "GET",
              dataType: "json",
              async: false,
              success: function(xhr){ info += "<tr><td>" + xhr.id + "</td>"; },
              error: function(xhr){ alert(xhr.responseText); },
              beforeSend: function(xhr){ xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034"); }
            });
            info += "<td>" + xhr.objects[i].qty_ordered + "</td></tr>";
          });
          info += '</tbody></table>';
          $("#po-info").html(info);
        },
        error: function(xhr){ alert(xhr.responseText); },
        beforeSend: function(xhr){ xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034"); }
      });

  });

  // listen for sku selection
  $(".sku").change(function(){
    var input = $(this);
    $.ajax({
      url: "/api/sku-service/skus/" + $(this).val() + "/",
      type: "GET",
      dataType: "json",
      success: function(xhr){
        var info = '<tr><td colspan=2><table class="table table-condensed"><tbody><tr>' +
          '<td class="col-xs-4"><b>Qty on Hand:</b> ' + xhr.qty_on_hand + '</td>' +
          '<td class="col-xs-4"><b>Location:</b> ' + xhr.location + '</td>' +
          '<td class="col-xs-4"><a target="_blank" href="/sku/' + xhr.id + '/">Detailed Info</a></td>' +
        '</tr></tbody></table></td></tr>';
        input.parent().parent().after(info);
      },
      error: function(xhr){ alert(xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034"); }
    });
  });

});
