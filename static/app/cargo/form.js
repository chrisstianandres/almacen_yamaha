var datatable;
var action = $('input[name="option"]').val();

var datos = {
    items: {
        nombre: '',
        modelos: []
    },
    fechas: {
        'action': action
    },
    add: function () {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: this.fechas,
            success: function (data) {
                datos.items.modelos = data;
                listar();
            }
        });
    }
};
$(document).ready(function () {
    validar_stilo();
    $("#form").validate({
        rules: {
            name: {
                required: true,
                minlength: 3,
                maxlength: 50,
            }
        },
        messages: {
            name: {
                required: "Por favor ingresa el nombre del rol",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
        },
    });

    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    $('#id_descripcion').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    datos.add();
    $('#datatable tbody')
        .on('change', 'input[name="ver"]', function (e) {
            e.preventDefault();
            var ver = $(this).is(':checked') ? 1 : 0;
            var tr = datatable.cell($(this).closest('td, li')).index();
            datos.items.modelos[tr.row].view = ver;
        })
        .on('change', 'input[name="agregar"]', function (e) {
            e.preventDefault();
            var agregar = $(this).is(':checked') ? 1 : 0;
            var tr = datatable.cell($(this).closest('td, li')).index();
            datos.items.modelos[tr.row].add = agregar;
        })
        .on('change', 'input[name="editar"]', function (e) {
            e.preventDefault();
            var editar = $(this).is(':checked') ? 1 : 0;
            var tr = datatable.cell($(this).closest('td, li')).index();
            datos.items.modelos[tr.row].change = editar;
        })
        .on('change', 'input[name="eliminar"]', function (e) {
            e.preventDefault();
            var eliminar = $(this).is(':checked') ? 1 : 0;
            var tr = datatable.cell($(this).closest('td, li')).index();
            datos.items.modelos[tr.row].delete = eliminar;
        });

    $('#form')
        .on('submit', function (e) {
                e.preventDefault();
                var parametros;
                datos.items.nombre = $('#id_name').val();
                parametros = {'permisos': JSON.stringify(datos.items)};
                parametros['action'] = 'add';
                var isvalid = $(this).valid();
                if (isvalid) {
                    submit_with_ajax_other(window.location.pathname, 'Alerta',
                        'Esta seguro que desea agregar este rol', parametros, function () {
                        window.location.href = '/cargo/lista/'
                    });
                }
            }
        );
});

function listar() {
    datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        search: false,
        destroy: true,
        info: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        data: datos.items.modelos,
        columns: [
            {"data": "num"},
            {"data": "nombre"},
            {"data": "view"},
            {"data": "add"},
            {"data": "change"},
            {"data": "delete"},
        ],

        dom:
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                width: '10%',
                orderable: false,
                render: function (data, type, row) {
                    if (row.nombre === 'empresa' || row.nombre === 'devolucion' || row.nombre === 'inventario'|| row.nombre === 'reportes') {
                        return ''
                    } else {
                        return data === 0 ? '<input type="checkbox" name="eliminar">' : '<input type="checkbox" checked="checked" name="eliminar">';
                    }
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                width: '10%',
                orderable: false,
                render: function (data, type, row) {
                    if (row.nombre === 'compra' || row.nombre === 'venta' || row.nombre === 'devolucion' || row.nombre === 'inventario' || row.nombre === 'reportes') {
                        return ''
                    } else {
                        return data === 0 ? '<input type="checkbox" name="editar">' : '<input type="checkbox" checked="checked" name="editar">';
                    }


                }
            },
            {
                targets: [-3],
                class: 'text-center',
                width: '10%',
                orderable: false,
                render: function (data, type, row) {
                    if (row.nombre === 'empresa' || row.nombre === 'inventario' || row.nombre === 'reportes') {
                        return '';
                    } else {
                        return data === 0 ? '<input type="checkbox" name="agregar">' : '<input type="checkbox" checked="checked" name="agregar">';
                    }


                }
            },
            {
                targets: [-4],
                class: 'text-center',
                width: '10%',
                orderable: false,
                render: function (data, type, row) {
                    return data === 0 ? '<input type="checkbox" name="ver">' : '<input type="checkbox" checked="checked" name="ver">';

                }
            },
        ]
    });

}