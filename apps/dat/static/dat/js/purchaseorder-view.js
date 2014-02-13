$(document).ready(function(){

  // get qtys ordered
  $('td.sku').each(function(i){
    var tdid = '#' + $(this).attr('sku') + '-qty';
    $.ajax({
      url: '/api/warehouse/shipment-products/?slug=' + $(this).attr('po') + '-' + $(this).attr('sku'),
      type: 'GET',
      dataType: 'json',
      success: function(xhr, status){
        $(tdid).html(xhr.objects[0].qty_received);
      },
      error: function(xhr, status){ alert(status + ' ' + xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey vince:51ec739d7e8e7a24381ebd8b8a10e6be79c33e54'); }
    });
  });

});
