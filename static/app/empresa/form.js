$(document).ready(function () {
    validar_stilo();
    jQuery.validator.addMethod("iva_check", function (value, element) {
        return value >= 0 && value <= 100;
        //[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
    }, "Debe ingresar una cantidad entre 0 y 100");
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            iva: {
                required: true,
                iva_check: true
            },
            ciudad: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            ruc: {
                required: true,
                minlength: 13,
                maxlength: 13,
                digits: true,
                validar: true
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
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar maximo 50 caracteres"
            },
            iva: {
                required: "Esta informacion es requerida"
            },
            ruc: {
                required: "Por favor ingresa tu numero de documento",
               minlength: "Debe ingresar 13 caracteres",
                maxlength: "Debe ingresar 13 caracteres"
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
    $('#id_nombre').keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras;

    $('#id_ruc').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

    $('#id_telefono').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

});


//.keypress(function (e) {
//         if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
//             return false;
//         }
//     });//Para solo numeros