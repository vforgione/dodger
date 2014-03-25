function cloneMore(selector, type) {
  var newElement = $(selector).clone(true);
  var total = $('#id_' + type + '-TOTAL_FORMS').val();
  newElement.find(':input').each(function() {
      var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
  });
  newElement.find('label').each(function() {
      var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
      $(this).attr('for', newFor);
  });
  total++;
  $('#id_' + type + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
}

$(document).ready(function () {

  $("#add-more").click(function(){
    cloneMore('div.formset:last', 'shipmentlineitem_set');
  });

  // global scope options
  var options = '<option></option>';

  // listen for change in po selection
  $('#id_purchase_order').change(function () {

    // get details on po
    $.ajax({
      url: '/api/sku_service/purchase_orders/' + $(this).val() + '/',
      type: 'GET',
      dataType: 'json',
      async: false,  // make blocking call
      success: function (xhr, status) {
        // set supplier to retrieve products
        var supplier_uri = xhr.supplier;
        $.ajax({
          url: supplier_uri,
          type: 'GET',
          dataType: 'json',
          async: false,  // make blocking call
          success: function (xhr, status) {
            $('#supplier').val(xhr.id);
          },
          error: function (xhr, status) {
            alert(status + ' ' + xhr.responseText);
          },
          beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
          }
        });
      },
      error: function (xhr, status) {
        alert(status + ' ' + xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
      }
    });

    // load up sku from supplier - the rationale is that the supplier could screw up and switch skus
    $.ajax({
      url: '/api/sku_service/skus/?supplier__id=' + $('#supplier').val(),
      type: 'GET',
      dataType: 'json',
      success: function (xhr, status) {
        $(xhr.objects).each(function (i) {
          options += '<option value="' + xhr.objects[i].id + '">' + xhr.objects[i].description + '</option>';
        });
      },
      error: function (xhr, status) {
        alert(status + ' ' + xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader('Authorization', 'ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034');
      },
      complete: function () {
        $('.sku').html(options);
      }
    });


    // load up info pane
    $.ajax({
      url: "/api/sku_service/purchase_order_line_items/?purchase_order__id=" + $(this).val(),
      type: "GET",
      dataType: "json",
      success: function (xhr) {
        var info = '<h4>PO Detail</h4><table class="table table-condensed"><thead><tr><th>SKU</th><th>Qty Ordered</th></tr></thead><tbody>';
        $(xhr.objects).each(function (i) {
          $.ajax({
            url: xhr.objects[i].sku,
            type: "GET",
            dataType: "json",
            async: false,
            success: function (xhr) {
              info += "<tr><td class='col-lg-6'>" + xhr.description + "</td>";
            },
            error: function (xhr) {
              alert(xhr.responseText);
            },
            beforeSend: function (xhr) {
              xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034");
            }
          });
          info += "<td class='col-lg-6'>" + xhr.objects[i].quantity_ordered + "</td></tr>";
        });
        info += '</tbody></table>';
        $("#po-info").html(info);
      },
      error: function (xhr) {
        alert(xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034");
      }
    });

  });

  // listen for sku selection
  $(".sku").change(function () {
    var input = $(this);
    var next = input.parent().parent().next();

    // wipe out any detail data if sku changes twice
    try {
      if (next.html().substr(0, 6) == "<td><a") {
        next.html("");
      }
    } catch (e) {}

    $.ajax({
      url: "/api/sku_service/skus/" + $(this).val() + "/",
      type: "GET",
      dataType: "json",
      success: function (xhr) {
        var info = '<tr class="detail-info">' +
          '<td><a target="_blank" href="/skus/' + xhr.id + '/">Detailed Info</a></td>' +
          '<td><b>Qty on Hand:</b> ' + xhr.quantity_on_hand +
          '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Location:</b> ' + xhr.location + '</td>' +
          '</tr>';
        input.parent().parent().after(info);
      },
      error: function (xhr) {
        alert(xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034");
      }
    });
  });

});
