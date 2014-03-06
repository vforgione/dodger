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
    cloneMore('div.formset:last', 'purchaseorderlineitem_set');
  });

  // listen for supplier choice
  $("#id_supplier").change(function () {
    // load contacts
    $.ajax({
      url: "/api/sku_service/contacts/?represents__id=" + $(this).val(),
      type: "GET",
      dataType: "json",
      success: function (xhr) {
        var options = "<option></option>";
        $(xhr.objects).each(function (i) {
          options += "<option value=\"" + xhr.objects[i].id + "\">" + xhr.objects[i].name + "</option>";
        });
        $("#id_contact").html(options);
      },
      error: function (xhr) {
        alert(xhr.responseText);
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034");
      }
    });
    // load up skus
    $.ajax({
      url: "/api/sku_service/skus/?supplier__id=" + $(this).val(),
      type: "GET",
      dataType: "json",
      success: function (xhr) {
        var options = "<option></option>";
        $(xhr.objects).each(function (i) {
          options += "<option value=\"" + xhr.objects[i].id + "\">" + xhr.objects[i].description + "</option>";
        });
        $(".sku").html(options);
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
          '<td><b>Qty on Hand:</b> ' + xhr.quantity_on_hand + '</td>' +
          '<td colspan="3"><b>Cost:</b> $' + xhr.cost + '</td>' +
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
