$(document).ready(function () {
   validar_stilo();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos tres letras del modelo",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },

        },
    });

     $("#formmodelo").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos tres letras del modelo",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },

        },
    });

    $('#id_nombre').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });

});