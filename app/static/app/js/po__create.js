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

});
