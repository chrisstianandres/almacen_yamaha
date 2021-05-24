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
                'action': 'searchdetalle',
            },
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        columns: [
            {"data": "fecha_compra"},
            {"data": "proveedor.nombres"},
            {"data": "comprobante"},
            {"data": "total"},
            {"data": "estado"},
            {"data": "id"},

        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var detalle = '<a type="button" class="btn btn-outline-success btn-sm btn-round" data-toggle="tooltip"title="Ver Detalle Compra" rel="detalle""><i class="fa fa-search"></i></a> ';
                    pdf = '<a type="button" class="btn btn-outline-danger btn-sm btn-round" href="/compra/factura/'+data+'" data-toggle="tooltip" title="Imprimir PDF" rel="pdf"><i class="fa fa-file-pdf"></i></a>';
                    return detalle + pdf;
                },
            },
            {
                targets: [-4],
                class: 'text-center'
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$ ' + data;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.estado === 'FINALIZADA') {
                        return '<span class=" badge badge-success"> ' + data + '</span>'
                    }
                    return '<span class=" badge badge-danger"> ' + data + '</span>'
                }
            },
        ]
    })
        .on('click', 'a[rel="detalle"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#tbldetalle').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'detalle',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
                },
                columns: [
                    {"data": "producto.nombre"},
                    {"data": "cantidad"},
                    {"data": "p_compra_actual"},
                    //{"data": "subtotal"},

                ],
                columnDefs: [

                    {
                        targets: [2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$ ' + data;
                        }
                    },
                ]
            })
            $('#Modal').modal('show');
        });
});
