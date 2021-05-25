$(document).ready(function () {
    $('#id_is_superuser').removeClass('form-control');
    validar_stilo();
    $("#form").validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            last_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            username: {
                required: true,
                minlength: 5,
                maxlength: 50,
                lettersonly: true,

            },
            email: {
                required: true,
                email: true,

            },
            password: {
                required: true,

            },
            telefono: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true
            },
            cedula: {
                required: true,
                digits: true,
                validar: true
            },
            direccion: {
                required: true,
                minlength: 7,
                maxlength: 100,
            },
            sexo: {
                required: true
            }
        },
        messages: {
            first_name: {
                required: "Esta infromacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Esta infromacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            username: {
                required: "Esta infromacion es requerida",
                minlength: "Debe ingresar al menos 5 caracteres",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            email: {
                required: "Esta infromacion es requerida",
                email: "Por favor ingrese un correo valido"

            },
            password: {
                required: "Por favor ingresar una contraseña",

            },
            telefono: {
                required: "Por favor ingresar un numero de celular",
                //minlength: "Debe ingresar al menos tres letras de tu cargo",
                digits: 'Porfavor ingresar solo numeros '
                //lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Esta infromacion es requerida",
                digits: 'Por favor ingresar solo numeros'
                //lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            direccion: {
                required: "Esta infromacion es requerida",
                minlength: "Debe ingresar al menos 7 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            sexo: {
                required: "Esta infromacion es requerida",
            }

        },
    });

    $('#id_first_name').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    $('#id_last_name').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    $('#id_direccion').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    $('.select2').select2({
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
        }
    });

});