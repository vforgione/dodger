function getReceived(id, po){
  $.ajax({
    url: "/api/sku_service/shipment_line_items/?sku__id=" + id + "&shipment__purchase_order__id=" + po,
    type: "GET",
    dataType: "json",
    success: function(xhr){
      console.log(xhr);
      var td = "#" + id;
      try {
        var qty = xhr.objects[0].quantity_received;
        var url = xhr.objects[0].shipment;
        url = url.substr(url.length - 2, 1);
        var html = '<a href="/shipments/' + url + '/" target="_blank">' + qty + '</a>';
        $(td).html(html);
      } catch (ex) {
        var td = "#" + id;
        $(td).html(0);
      }
    },
    error: function (xhr, ajaxOptions, thrownError) {
      var td = "#" + id;
      $(td).html(0);
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "ApiKey api-readonly:697ccf3beb1cc60c1eddaa8bc6ef9fc968661034");
    }
  });
}

$(document).ready(function(){
  var po = $("#po").val();
  $(".rcvd").each(function(){
    getReceived($(this).attr('id'), po);
  });
});
