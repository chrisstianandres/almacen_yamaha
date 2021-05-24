$(document).ready(function () {
    validar_stilo();
    $("#form").validate({
        rules: {
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            apellidos: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            cedula: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true,
                validar: true
            },
            correo: {
                required: true,
                email: true
            },
            edad:{
                required: true,
                mayoredad: true
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
            nombres: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            apellidos: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            edad:{
                required: 'La edad es requerida'
            },
            cedula: {
                required: "Esta informacion es requerida",
                minlength: "Tu numero de cedula debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de cedula debe tener maximo 10 digitos",
                validar: "Numero de cedula no valido"
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

    $('#id_nombres').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    }).keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras
    $('#id_apellidos').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    }).keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras

    $('#id_cedula').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros
    $('#id_telefono').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

    $('#id_edad').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

});