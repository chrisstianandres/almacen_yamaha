$(function () {
    validar_stilo();
    $("#formlogin").validate({
        rules: {
            username: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            password: {
                required: true,
                minlength: 3,
                maxlength: 50
            },


        },
        messages: {
            username: {
                required: "El usuario es requerido",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar maximo 50 caracteres",
            },
            password: {
                required: "Debe ingresar una contraseña",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar maximo 50 caracteres",
            }
        },
    });
    $('#formlogin').on('submit', function (e) {
        e.preventDefault();
        var valid = $(this).valid();
        if (valid) {
            var parametros;
            parametros = {
                'username': $('input[name="username"]').val(),
                'password': $('input[name="password"]').val()
            };
            login('/login/connect/', parametros, function () {
                let timerInterval;
                Swal.fire({
                    title: 'Iniciando Sesion!',
                    timer: 2000,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading()
                    },
                    willClose: () => {
                        clearInterval(timerInterval)
                    }
                }).then((result) => {
                    /* Read more about handling dismissals below */
                    if (result.dismiss === Swal.DismissReason.timer) {
                        console.log('I was closed by the timer')
                    }
                });
                setTimeout(function () {
                    location.href = '/dashbord';
                }, 2000);

            });
        }
    });
});

