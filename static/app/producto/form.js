$(document).ready(function () {
    validar_stilo();
    jQuery.validator.addMethod("prec", function (value, element) {
        return value >= 0.5;
    }, "algo");
     jQuery.validator.addMethod("precio_venta", function (value, element) {
        return parseFloat(value) > parseFloat($('#id_pvp').val());
    }, "");

    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
            },

            marca: {
                required: true,
            },
            modelo: {
                required: true,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 80,
                //digits: true
            },
            pvp: {
                required: true,
                prec: true
            },
            p_venta: {
                required: true,
                precio_venta: true
            },

        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                maxlength: "Debe ingresar maximo 50 letras",
            },
            marca: {
                required: "Esta informacion es requerida",
            },
            modelo: {
                required: "Esta informacion es requerida",
            },
            descripcion: {
                required: "Esta informacion es requerida",
                minlength: "Escribe al menos 5 caracteres ",
                maxlength: "Maxmimo 80 caracteres",
            },
            pvp: {
                required: "Esta informacion es requerida",
                prec: "Debe ingresar un valor de al menos 0.5 dolares"
            },
            p_venta: {
                required: "Esta informacion es requerida",
                precio_venta: "Debe ingresar un valor mayor al precio de compra"
            },

        },
    });

    // agregar marca modal envento click boton
    $('#btnaddmarca').on('click', function () {
        //presentar modal de proveedor
        $('#mymodalmarca').modal('show');
    });

    $('#formmarca').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_marca');
            submit_with_ajax('/marca/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalmarca').modal('hide');
                var newOption = new Option(response.marca['full'], response.marca['id'], false, true);
                $('select[name="marca"]').append(newOption).trigger('change');
            });
        }

    });

    // agregar modelo modal envento click boton
    $('#btnaddmodelo').on('click', function () {
        //presentar modal de proveedor
        $('#mymodalmodelo').modal('show');
    });

    $('#formmodelo').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_modelo');
            submit_with_ajax('/modelo/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalmodelo').modal('hide');
                var newOption = new Option(response.modelo['full'], response.modelo['id'], false, true);
                $('select[name="modelo"]').append(newOption).trigger('change');
            });
        }

    });

    $('#id_nombre').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    $('#mymodalmarca').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        reset('#formmarca');
    });
    $('#mymodalmodelo').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        reset('#formmodelo');
    });
    });