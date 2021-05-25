$(function () {
    var datatable = $('#example1').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'inventario'
            },
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        columns: [
            {"data": "nombre"},
            {"data": "marca.nombre"},
            {"data": "modelo.nombre"},
            {"data": "pvp"},
            {"data": "stock"},

        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data >= 6) {
                        return '<span class=" badge badge-success"> ' + data + '</span>'
                    }
                    return '<span class=" badge badge-danger"> ' + data + '</span>'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + data
                }
            },
        ]
    });
});