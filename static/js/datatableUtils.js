function dibujarTabla(table, response) {
    table.clear().draw();
    entradas = Object.keys(response["items"])
    items = response["items"]
    for (var i = 0; i < entradas.length; i++) {
        table.row.add([
            items[i]["id"],
            items[i]["usuario_id"],
            "Camiseta",
            items[i]["created_at"],
            items[i]["tipo_pago_id"],
            items[i]["subtotal"],
            items[i]["iva"],
            items[i]["valor_total"],
        ]);
    }
    totales = response["totales"]
    table.row.add(["", "", "", "", "", totales.subtotal, totales.iva, totales.total])
    table.draw();
    $('#boton').prop("disabled", false);
}
function dateRangeInit(nombre) {
    var d = new Date();
    var day = d.getDate
    $('input[name='+nombre+']').daterangepicker({
        "locale": {
            "applyLabel": "Aceptar",
            "cancelLabel": "Cancelar",
            "daysOfWeek": [
                "Lu",
                "Ma",
                "Mi",
                "Ju",
                "Vi",
                "Sá",
                "Do"
            ],
            "monthNames": [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre"
            ],
        },
        opens: 'left',
        startDate: day,
        endDate: moment().add('days', 7).format('L')
    });
}

function tableInit(tagId) {
    var table = $(tagId).DataTable({
        order: false,
        dom: 'Bfrtip',
        buttons: [
            'excel', 'pdf', 'print'
        ],
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'Pdf',
                className: 'btn btn-info btn-flat btn-xs'
            },
            {
                extend: 'print',
                text: 'Imprimir <i class="fas fa-print"></i>',
                titleAttr: 'Print',
                className: 'btn btn-secondary btn-flat btn-xs'
            },
        ],
        language: {
            "decimal": "",
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ entrada(s)",
            "infoEmpty": "Mostrando 0 entradas",
            "infoFiltered": "(Filtrado de _MAX_ entradas totales)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ entradas",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscar:",
            "zeroRecords": "Sin resultados encontrados",
            "paginate": {
                "first": "Primero",
                "last": "Ultimo",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        },

    });
    return table;
};