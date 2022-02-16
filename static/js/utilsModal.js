function openModelWithContext(event) {
  var target = $(this).data('target');
  var url_activar = $(this).data('url-activar');
  var url_eliminar = $(this).data('url-eliminar');
  var action = $(this).data('action');
  var success = $(this).data('success');
  var url = $(this).is(':checked') ? url_activar : url_eliminar;
  $.ajax({
    url: url,
    data: {
      action: action,
      success: success,
    },
    success: function (data) {
      $(target + ' .modal-content').html(data);
      $(target).modal('show');
    },
  });

  $(target).on('hide.bs.modal', () => {
    var return_og = $(this).is(':checked') ? 'off' : 'on';
    $(this).bootstrapToggle(return_og, true);
  });
}

$(document).on('change', '.use-modal', openModelWithContext);
