function menssaje_error(title, obj, icon) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }

    Swal.fire({
        title: title,
        html: html,
        icon: 'error'
    });
}

//submit para guardar datos
function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        processData: false,
                        contentType: false,
                        data: parameters,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        menssaje_error('Error', data.error, 'fas fa-exclamation-circle');

                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

//submit para eliminar en tabla
function submit_with_ajax_other(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parameters,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        menssaje_error('Error', data.error, 'fas fa-exclamation-circle');

                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function validar_stilo() {
    $.validator.setDefaults({
        errorClass: 'invalid-feedback',

        highlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-invalid")
                .removeClass("is-valid");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-valid")
                .removeClass("is-invalid");
        }
    });


    jQuery.validator.addMethod("validar", function (value, element) {
        return validar(element);
    }, "Número de documento no valido para Ecuador");

    function validar(element) {
        var cad = document.getElementById(element.id).value.trim();
        var total = 0;
        var longitud = cad.length;
        var longcheck = longitud - 1;
        if (longitud === 10) {
            return aux(total, cad);
        } else if (longitud === 13 && cad.slice(10, 13) !== '000') {
            return aux(total, cad);
        } else {
            return false;
        }
    }

    function aux(total, cad) {
        if (cad !== "") {
            for (var i = 0; i < 9; i++) {
                if (i % 2 === 0) {
                    var aux = cad.charAt(i) * 2;
                    if (aux > 9) aux -= 9;
                    total += aux;
                } else {
                    total += parseInt(cad.charAt(i)); // parseInt o concatenará en lugar de sumar
                }
            }

            total = total % 10 ? 10 - total % 10 : 0;
            return parseInt(cad.charAt(9)) === total;
        }
    }

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/i.test(value);
        //[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
    }, "Letters and spaces only please");

    jQuery.validator.addMethod("mayoredad", function (value, element) {
        return value >= 18 && value <= 60;
        //[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
    }, "Debe ingresar un edad entre 18 y 60 años");

}


function borrar_todo_alert(title, content, callback) {
    $.confirm({
        title: title,
        icon: 'fas fa-exclamation-triangle',
        type: 'red',
        typeAnimated: true,
        content: content,
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red'
            },
        }
    });
}

// function menssaje_error(title, content, icon, callback) {
//     var obj = $.confirm({
//         theme: 'modern',
//         icon: icon,
//         title: title,
//         type: 'red',
//         content: content,
//         draggable: true,
//         buttons: {
//             info: {
//                 text: '<i class="fas fa-check"></i> Ok',
//                 btnClass: 'btn-blue'
//             },
//         }
//     });
//     setTimeout(function () {
//         // some point in future.
//         obj.close();
//     }, 3000);
// }

function menssajeok(title, content, icon, callback) {
    var obj = $.confirm({
        theme: 'modern',
        icon: 'far fa-grin-beam',
        title: title,
        type: 'blue',
        content: content,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }
            },
        }
    });
}

function printpdf(title, content, callback, cancel) {
    $.confirm({
            theme: 'modern',
            type: 'blue',
            icon: 'fas fa-exclamation-circle',
            title: title,
            content: content,
            columnClass: 'small',
            draggable: true,
            buttons: {
                si: {
                    text: '<i class="fas fa-check"></i> Si',
                    btnClass: 'btn-blue',
                    action: function () {
                        callback();
                    }
                },
                no: {
                    text: '<i class="fas fa-times"></i> No',
                    btnClass: 'btn-red',
                    action: function () {
                        cancel();
                    }
                }
            }
        }
    );
}

function save_estado(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        icon: 'fas fa-exclamation-circle',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        menssaje_error(data.error, data.content, 'fa fa-times-circle');
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                    //

                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {
                }
            }
        }
    });
}

function login(url, parametros, callback) {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: url,
        data: parametros,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            callback();
            return false;
        }
        var error = data.error;
        menssaje_error(error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    })
}

function reset(formulario) {
    $(formulario)[0].reset();
    var validator = $(formulario).validate();
    validator.resetForm();
    $('.is-valid').removeClass('is-valid');
    $('.is-invalid').removeClass('is-invalid');
}