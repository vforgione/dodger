// disable sku select
$('#id_sku').prop('disabled', true);

// get skus
$.ajax({
  url: '/api/sku_service/skus/?supplier__id=' + $('#supplier-pk').val() + '&limit=0',
  type: 'GET',
  dataType: 'json',
  success: function (xhr, status) {
    var options= '<option></option>';
    $(xhr.objects).each(function (i) {
      options += '<option value="' + xhr.objects[i].id + '">' + xhr.objects[i].description + '</option>';
    });
    var sku = $('#id_sku');
    sku.html(options);
    sku.prop('disabled', false);
    sku.val($('#old-sku').val());
    $('#sku-warning').fadeOut(100);
  },
  error: function (xhr, status) {
    alert(status + ' ' + xhr.responseText);
  },
  beforeSend: function (xhr) {
    xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
  }
});

// set qty placeholder
$('#id_quantity_ordered').attr('placeholder', 'Previously Entered Qty: ' + $('#old-qty').val());
