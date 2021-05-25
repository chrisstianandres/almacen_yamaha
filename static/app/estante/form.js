$(document).ready(function () {
   validar_stilo();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 1,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 1 caracter"
            }
        }
    });

     $("#formestante").validate({
       rules: {
            nombre: {
                required: true,
                minlength: 1,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 1 caracter"
            }
        }
    });
});