$('#btn-one').click(function() {
  $('#btn-one').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Loading...').addClass('disabled');
});

$('#btn-dos').click(function() {
  $('#btn-dos').html('<span class="spinner-grow spinner-w-sm" role="status" aria-hidden="true" style="width: 1rem; height:1rem;"></span> Creando...').addClass('disabled');
});



