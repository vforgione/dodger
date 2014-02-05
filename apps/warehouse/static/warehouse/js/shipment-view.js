$(document).ready(function(){

  // get qtys ordered
  $('td.sku').each(function(i){
    var tdid = '#' + $(this).attr('po') + '-' + $(this).attr('sku') + '-qty';
    $.ajax({
      url: '/api/dat/purchase-order-products/?product__sku=' + $(this).attr('sku') + '&purchase_order__id=' + $(this).attr('po'),
      type: 'GET',
      dataType: 'json',
      success: function(xhr, status){
        $(tdid).html(xhr.objects[0].qty_ordered);
      },
      error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
    });
  });

});
