$(document).ready(function(){

  // listen for supplier choice
  $("#id_supplier").change(function(){
    // load contacts
    $.ajax({
      url: "/api/sku-service/contacts/?represents__id=" + $(this).val(),
      type: "GET",
      dataType: "json",
      success: function(xhr){
        var options = "<option></option>";
        $(xhr.objects).each(function(i){
          options += "<option value=\"" + xhr.objects[i].id + "\">" + xhr.objects[i].name + "</option>";
        });
        $("#id_contact").html(options);
      },
      error: function(xhr){ alert(xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034"); }
    });
    // load up skus
    $.ajax({
      url: "/api/sku-service/skus/?supplier__id=" + $(this).val(),
      type: "GET",
      dataType: "json",
      success: function(xhr){
        var options = "<option></option>";
        $(xhr.objects).each(function(i){
          options += "<option value=\"" + xhr.objects[i].id + "\">" + xhr.objects[i].description + "</option>";
        });
        $(".sku").html(options);
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
        var info = '<tr>' +
          '<td class="col-xs-3"><b>Qty on Hand:</b> ' + xhr.qty_on_hand + '</td>' +
          '<td class="col-xs-3"><b>Cost:</b> $' + xhr.cost + '</td>' +
          '<td class="col-xs-3" colspan="2"><a target="_blank" href="/sku/' + xhr.id + '/">Detailed Info</a></td>' +
        '</tr>';
        input.parent().parent().after(info);
      },
      error: function(xhr){ alert(xhr.responseText); },
      beforeSend: function(xhr){ xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034"); }
    });
  });

});
