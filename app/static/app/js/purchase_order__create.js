$(document).ready(function () {

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
    if (next.html().substr(0, 6) == "<td><a") {
      next.html("");
    }

    $.ajax({
      url: "/api/sku_service/skus/" + $(this).val() + "/",
      type: "GET",
      dataType: "json",
      success: function (xhr) {
        var info = '<tr>' +
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
