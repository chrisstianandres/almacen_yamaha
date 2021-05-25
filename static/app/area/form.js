$(document).ready(function () {
   validar_stilo();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras"
            }
        }
    });

     $("#formarea").validate({
       rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras"
            }
        }
    });
});