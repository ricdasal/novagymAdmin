const config = {
  autoUpdateInput: false,
  showDropdowns: true,
  locale: {
    format: 'DD/MM/YYYY',
    separator: ' - ',
    applyLabel: 'Aceptar',
    cancelLabel: 'Cancelar',
    fromLabel: 'Desde',
    toLabel: 'Hasta',
    weekLabel: 'Sem',
    daysOfWeek: ['DO', 'LU', 'MA', 'MI', 'JU', 'VI', 'SA'],
    monthNames: [
      'Enero',
      'Febrero',
      'Marzo',
      'Abril',
      'Mayo',
      'Junio',
      'Julio',
      'Agosto',
      'Septiembre',
      'Octubre',
      'Noviembre',
      'Diciembre',
    ],
    firstDay: 1,
  },
};

const configSingle = {
  ...config,
  singleDatePicker: true,
};

function _init_date() {
  $('.dateinput')
    .daterangepicker(configSingle)
    .on('apply.daterangepicker', function (ev, picker) {
      let date = picker.startDate.format('DD/MM/YYYY');
      $(this).val(date);
    })
    .on('cancel.daterangepicker', function (ev, picker) {
      $(this).val('');
    });
}

function _init_daterange() {
  $('.daterange')
    .daterangepicker(config)
    .on('apply.daterangepicker', function (ev, picker) {
      if (picker) {
        let start_date = picker.startDate;
        let end_date = picker.endDate;
        let field = $(this).data('field');
        $(`input[name=${field}_min]`).val(start_date.format('YYYY-MM-DD'));
        $(`input[name=${field}_max]`).val(end_date.format('YYYY-MM-DD'));
        $(this).val(`${start_date.format('DD/MM/YYYY')} - ${end_date.format('DD/MM/YYYY')}`);
      }
    })
    .on('cancel.daterangepicker', function (ev, picker) {
      $(this).val('');
      let field = $(this).data('field');
      $(`input[name=${field}_min]`).val('');
      $(`input[name=${field}_max]`).val('');
    });
}

function _init_() {
  _init_date();
  _init_daterange();
}

$(document).ready(_init_);
