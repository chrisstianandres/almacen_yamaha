$(document).ready(function () {
    validar_stilo();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
            },

            area: {
                required: true,
            },
            estante: {
                required: true,
            }
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                maxlength: "Debe ingresar maximo 50 letras",
            },
            area: {
                required: "Esta informacion es requerida",
            },
            estante: {
                required: "Esta informacion es requerida",
            }
        },
    });

    // agregar marca modal envento click boton
    $('#btnaddarea').on('click', function () {
        //presentar modal de proveedor
        $('#mymodalarea').modal('show');
    });

    $('#formarea').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_area');
            submit_with_ajax('/area/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalarea').modal('hide');
                var newOption = new Option(response.area['nombre'], response.area['id'], false, true);
                $('select[name="area"]').append(newOption).trigger('change');
            });
        }

    });

    // agregar modelo modal envento click boton
    $('#btnaddestante').on('click', function () {
        //presentar modal de proveedor
        $('#mymodalestante').modal('show');
    });

    $('#formestante').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_estante');
            submit_with_ajax('/estante/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodalestante').modal('hide');
                var newOption = new Option(response.estante['nombre'], response.estante['id'], false, true);
                $('select[name="estante"]').append(newOption).trigger('change');
            });
        }

    });

    $('#mymodalestante').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        reset('#formestante');
    });
    $('#mymodalarea').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        reset('#formarea');
    });


    });