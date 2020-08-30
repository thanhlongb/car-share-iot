$(document).ready(function(){
  $("#search-text").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#search-table tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
