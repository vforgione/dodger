$(function () {

  var sku = $("#id-sku-lookup");
  sku.autocomplete({
    source: function (term, callback) {
      $.ajax({
        url: "/api/sku_service/skus/?id__icontains=" + term.term,
        type: 'GET',
        dataType: 'json',
        success: function (xhr) {
          var res = [];
          $(xhr.objects).each(function (i) {
            var val = xhr.objects[i].description.substr(1, 5);
            res.push(val);
          });
          callback(res);
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
        }
      });
    },
    minLength: 3
  });

  // listen for change to sku selection - add placeholder with current qty to 'new' field
  sku.focusout(function () {
    $.ajax({
      url: '/api/sku_service/skus/' + $(this).val() + '/',
      type: 'GET',
      dataType: 'json',
      success: function (xhr) {
        var html ='<div class="form-group"><input type="checkbox" id="sku-' + xhr.id + '" name="skus" value="' + xhr.id + '" checked />' +
                  '<label for="sku-' + xhr.id + '">&nbsp;&nbsp;&nbsp;' +
                  xhr.description + ' | ' + xhr.quantity_on_hand + ' | ' + xhr.location + '</label></div>';
        $('#skus').append(html);
      },
      error: function (xhr) {
        alert(xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
      }
    });
  });

});
