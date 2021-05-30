var datatable, tbldetalle;
var compras = {
    items: {
        proveedor: '',
        cantidad: '',
        pvp: '',
        fecha_compra: '',
        comprobante: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        estado: '',
        producto: []

    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.producto, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    //agregar los productos
    add: function (item) {
        this.items.producto.push(item);
        this.list();
    },
    //calcular
    calculate: function () {
        var subtotal = 0.00;
        $.each(this.items.producto, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        this.items.total = subtotal;
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    list: function () {
        console.log(compras.items.producto);
        this.calculate();
        datatable = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            // dom: 'ltip',
            data: this.items.producto,
            columns: [
                {"data": "id"},
                {"data": "nombre_full"},
                {"data": "id"},
                {"data": "cantidad"},
                {"data": "pvp"},
                {"data": "subtotal"},
            ],
            language: {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast": "Último",
                    "sNext": "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            },
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var select = '<select name="ubicacion" class="form-control select2">';
                        select += '<option value="' + row.ubicacion_id + '" selected="selected">' + row.ubicacion_text + '';
                        $.each(row.ubicacion, function (key, value) {
                            select += '<option value="' + value.id + '">' + value.nombre + '';
                        });
                        select += '</select>';

                        return select
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm " autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback: function (row, data) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });//Para solo numeros
            }
        });
    }
};
$(function () {
    compras.list();

    $('#fecha_compra').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD"),
        minDate: moment().format("YYYY-MM-DD"),

    });

    $("input[name='iva']").prop('readonly', true);


    // buscar productos

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(compras.get_ids())
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                menssaje_error(textStatus, errorThrown)
            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            compras.add(ui.item);
            $(this).val('');
        }
    });

    // agregar proveedor modal envento click boton
    $('#btnaddproveedor').on('click', function () {
        //presentar modal de proveedor
        $('#mymodalproveedor').modal('show');
    });

    $('#buscar_producto').on('click', function () {
        tbldetalle = $('#tbldetalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'detalle',
                    'ids': JSON.stringify(compras.get_ids())
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
                {"data": "id"}

            ],
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',

                },
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="select" ' +
                            'data-toggle="tooltip" title="Seleccionar producto"><i class="fa fa-arrow-circle-right"></i></a>';
                    }
                },
            ]
        });
        $('#mymodalproducto').modal('show');
    });

    $('#tbldetalle tbody').on('click', 'a[rel="select"]', function () {
        var tr = tbldetalle.cell($(this).closest('td, li')).index();
        var data = tbldetalle.row(tr.row).data();
        compras.add(data);
        $('#mymodalproducto').modal('hide');

    });

    $('#formproveedor').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_compra');
            submit_with_ajax('/proveedor/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalproveedor').modal('hide');
                var newOption = new Option(response.proveedor['full'], response.proveedor['id'], false, true);
                $('select[name="proveedor"]').append(newOption).trigger('change');
            });
        }

    });

    //buscar proveedor
    $('select[name="proveedor"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_proveedor'
                };
            },
            processResults: function (data) {
                return {
                    results: data

                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    });

    $('.btnRemoveAll').on('click', function () {
        if (compras.items.producto.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar estos productos de su detalle <br> ' +
            '<strong>CONTINUAR?</strong>', function () {
                compras.items.producto = [];
                compras.list();
            });
    });


    //eliminar productos del detalle
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar este producto de tu detalle <br> ' +
                '<strong>CONTINUAR?</strong>', function () {
                    compras.items.producto.splice(tr.row, 1);
                    compras.list();
                });

        })
        //calcular el subtotal
        .on('change keyup', 'input[name="cant"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = datatable.cell($(this).closest('td, li')).index();
            compras.items.producto[tr.row].cantidad = cantidad;
            compras.calculate();
            $('td:eq(5)', datatable.row(tr.row).node()).html('$' + compras.items.producto[tr.row].subtotal.toFixed(2));
        })
        .on('change keyup', 'select[name="ubicacion"]', function () {
            var ubicacion = parseInt($(this).val());
            var text = $(this).find('option:selected').text();
            var tr = datatable.cell($(this).closest('td, li')).index();
            compras.items.producto[tr.row].ubicacion_id = ubicacion;
            compras.items.producto[tr.row].ubicacion_text = text;
        });
    $('#save').on('click', function () {
        if ($('select[name="proveedor"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un proveedor", 'far fa-times-circle');
            return false
        } else if ($('input[name="comprobante"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar un numero de comprobante", 'far fa-times-circle');
            return false
        } else if (compras.items.producto.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
        }
        compras.items.fecha_compra = $('input[name="fecha_compra"]').val();
        compras.items.comprobante = $('#id_comprobante').val();
        compras.items.proveedor = $('#id_proveedor option:selected').val();
        //compra.items.estado = $('#id_estado option:selected').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('compra', JSON.stringify(compras.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/compra/lista/';
        });
    });

    compras.list();
});

