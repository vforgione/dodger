$(document).ready(function(){

  // add classes to check boxes
  $('#id_notify_at_threshold').addClass('form-control');
  $('#id_in_live_deal').addClass('form-control');
  $('#id_is_subscription').addClass('form-control');

  $('.del-btn').each(function () {
    var val_id = '#id_skuattribute_set-' + (parseInt(this.id) - 1) + '-id'
      , val = $(val_id).val();
    $(this).attr('href', '/sku_attributes/delete/' + val + '/');
  });

});
