$(document).ready(function () {
    validar_stilo();
    $.validator.addMethod("tipo", function (value, element) {

        var tipo = $("#id_tipo_doc").val();
        if (tipo === '0') {
            return ((value.length === 13));
        } else if (tipo === '1') {
            return ((value.length === 10));
        }
    }, "");
    $("#form").validate({
        rules: {
            razon_social: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            numero_doc: {
                required: true,
                tipo: true,
                validar: true,
                digits: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },
        },
        messages: {
            razon_social: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            nombres: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            numero_doc: {
                required: "Esta informacion es requerida",
                tipo: "Tu numero de documento debe tener al menos 10 digitos para cedula y 13 digitos para ruc",
                digits: "Debe ingresar unicamente numeros",
                validar: "Tu numero de documento no es valido",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Esta informacion es requerida",
                minlength: "Tu numero de celular debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de celular debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Esta informacion es requerida",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $("#formproveedor").validate({
        rules: {
            razon_social: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            numero_doc: {
                required: true,
                tipo: true,
                validar: true,
                digits: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },
        },
        messages: {
            razon_social: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            nombres: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            numero_doc: {
                required: "Esta informacion es requerida",
                tipo: "Tu numero de documento debe tener al menos 10 digitos para cedula y 13 digitos para ruc",
                digits: "Debe ingresar unicamente numeros",
                validar: "Tu numero de documento no es valido",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Esta informacion es requerida",
                minlength: "Tu numero de celular debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de celular debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Esta informacion es requerida",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_razon_social')
        .keyup(function () {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        })
        .keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras
    $('#id_nombres')
        .keyup(function () {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        })
        .keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras


    $('#id_telefono').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros


    $('#id_numero_doc').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

});