var datatable, tbldetalle;
var venta = {
    items: {
        cliente: '',
        cantidad: '',
        pvp: '',
        fecha_venta: '',
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
        var indice = $('input[name="indice"]').val();
        var subtotal = 0.00;
        $.each(this.items.producto, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.p_venta);
            subtotal += dict.subtotal;
        });
        var iva_p = $('input[name="iva_empresa"]').val();
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva_p / 100;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    list: function () {
        this.calculate();
        datatable = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,

            data: this.items.producto,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "marca.nombre"},
                {"data": "modelo.nombre"},
                {"data": "stock"},
                {"data": "cantidad"},
                {"data": "p_venta"},
                {"data": "subtotal"},
            ],
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            },
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,

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
                    max: data.stock,
                    step: 1
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                }).on('keyup', function () {
                    if ($(this).val() > data.stock) {
                        menssaje_error('Error con el stock', 'No puedes ingresar una cantidad mayor al stock disponible', '');
                    }
                });//Para solo numeros
            }
        });
    }
};
$(function () {
    venta.list();

    $('#fecha_venta').datetimepicker({
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
                    'ids': JSON.stringify(venta.get_ids())
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                menssaje_error('Error!', textStatus + ': ' + errorThrown, '');
            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            venta.add(ui.item);
            $(this).val('');
        }
    });

    // agregar cliente modal envento click boton
    $('#btnaddcliente').on('click', function () {
        //presentar modal de cliente
        $('#mymodalcliente').modal('show');
    });

    //modal de tabla de productos
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
                    'ids': JSON.stringify(venta.get_ids())
                    //'id': data.id
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
                {"data": "stock"},
                {"data": "id"},

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
                        return row.stock >= 1 ? '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="select" ' +
                            'data-toggle="tooltip" title="Seleccionar producto"><i class="fa fa-arrow-circle-right"></i></a>' : ' '

                    }
                },
            ]
        });
        $('#mymodalproducto').modal('show');
    });

    $('#tbldetalle tbody').on('click', 'a[rel="select"]', function () {
        var tr = tbldetalle.cell($(this).closest('td, li')).index();
        var data = tbldetalle.row(tr.row).data();
        venta.add(data);
        $('#mymodalproducto').modal('hide');

    });

    $('#formcliente').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'create_cliente');
            submit_with_ajax(window.location.pathname, 'Notificación',
                '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalcliente').modal('hide');
                var newOption = new Option(response.cliente['full'], response.cliente['id'], false, true);
                $('select[name="cliente"]').append(newOption).trigger('change');
            });
        }

    });


    //buscar cliente
    $('select[name="cliente"]').select2({
        theme: "bootstrap4",
        language: {
            inputTooShort: function () {
                return "Ingresa al menos un caracter...";
            },
            "noResults": function () {
                return "Sin resultados";
            },
            "searching": function () {
                return "Buscando...";
            }
        },
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_cliente'
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
        if (venta.items.producto.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar estos productos de su detalle <br> ' +
            '<strong>CONTINUAR?</strong>', function () {
                venta.items.producto = [];
                venta.list();
            });
    });


    //eliminar productos del detalle
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar este producto de tu detalle <br> ' +
                '<strong>CONTINUAR?</strong>', function () {
                    venta.items.producto.splice(tr.row, 1);
                    venta.list();
                });

        })
        //calcular el subtotal
        .on('change keyup', 'input[name="cant"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = datatable.cell($(this).closest('td, li')).index();
            venta.items.producto[tr.row].cantidad = cantidad;
            venta.calculate();
            $('td:eq(6)', datatable.row(tr.row).node()).html('$' + venta.items.producto[tr.row].subtotal.toFixed(2));
        });


    $('#save').on('click', function () {
        if ($('select[name="cliente"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un cliente", 'far fa-times-circle');
            return false
        } else if (venta.items.producto.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
        }
        venta.items.fecha_venta = $('input[name="fecha_venta"]').val();
        venta.items.cliente = $('#id_cliente option:selected').val();
        //compra.items.estado = $('#id_estado option:selected').val();
        var parameters = new FormData();
        parameters.append('action', 'add');
        parameters.append('venta', JSON.stringify(venta.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters,
            function (response) {
                printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
                    window.open('/venta/printpdf/' + response['id'], '_blank');
                    location.href = '/venta/lista/';
                }, function () {
                    location.href = '/venta/lista/';
                })
            });
    });
    venta.list();


});

