$(document).ready(function(){

  // listen for change to sku selection - add placeholder with current qty to 'new' field
  $('#id_sku').change(function(){
    $.ajax({
      url: '/api/sku-service/skus/' + $(this).val() + '/',
      type: 'GET',
      dataType: 'json',
      success: function(xhr){ $('#id_new').attr('placeholder', 'Current Qty: ' + xhr.qty_on_hand); },
      error: function(xhr){ alert(xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034'); }
    });
  });

});
