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
                'action': 'searchdata',

            },
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        columns: [
            {"data": "id"},
            {"data": "full_name"},
            {"data": "username"},
            {"data": "email"},
            {"data": "date_joined"},
            {"data": "groups"},
            {"data": "foto"},
            {"data": "id"},

        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var editar = '<a type="button" class="btn btn-outline-success btn-sm btn-round" data-toggle="tooltip"title="Editar Datos" href="/usuario/editar/' + data + '"><i class="fa fa-edit"></i></a> ';
                    borrar = '<a type="button" class="btn btn-outline-danger btn-sm btn-round" data-toggle="tooltip" title="Eliminar Datos" rel="delete"><i class="fa fa-trash"></i></a>';
                    return editar + borrar;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" width="50" height="50" class="img-circle elevation-2" alt="User Image">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-success">' + value.name + '</span> ';
                    });
                    return html;
                }
            },
        ]
    });

    $('#example1 tbody')
        .on('click', 'a[rel="delete"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'delete'};
            submit_with_ajax_other(window.location.pathname, 'Alerta de Eliminacion!',
                'Esta seguro que desea borrar este usuario', parametros, function () {
                    datatable.ajax.reload(null, false);
                })
        })
});