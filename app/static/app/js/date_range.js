$(document).ready(function () {
  $('#start').change(function () {
    if ($(this).val() != '') {
      $('#end').prop('required', true);
    } else {
      $('#end').prop('required', false);
    }
  });
});
