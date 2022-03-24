function onSubmitForm(e) {
  e.preventDefault();
  $(this).attr('disabled', true).closest('form').trigger('submit');
}

$(document).on('click', '[type="submit"]', onSubmitForm);
