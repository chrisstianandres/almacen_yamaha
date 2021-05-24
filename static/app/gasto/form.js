$(document).ready(function () {
    validar_stilo();
    $("#form").validate({
        rules: {
            detalle: {
                required: true,
                minlength: 3,
                maxlength: 50
            },

            valor: {
                required: true,
            },
        },
        messages: {
            detalle: {
                required: "Esta informacion es requerida",
                minlength: "Debe ingresar al menos 3 letras",
            },
        },
    });

    // agregar marca modal envento click boton
    $('#btnaddtipogasto').on('click', function () {
        //presentar modal de proveedor
        $('#mymodaltipogasto').modal('show');
    });

    $('#formtipogasto').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            parameters.append('action', 'add_tipo_gasto');
            submit_with_ajax('/tipo_gasto/crear/', 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                $('#mymodaltipogasto').modal('hide');
                var newOption = new Option(response.tipo_gasto['full'], response.tipo_gasto['id'], false, true);
                $('select[name="tipo_gasto"]').append(newOption).trigger('change');
            });
        }

    });

$('#fecha').datetimepicker({
    format: 'YYYY-MM-DD',
    date: moment().format("YYYY-MM-DD"),
    locale: 'es',
    maxDate: moment().format("YYYY-MM-DD"),
    minDate: moment().format("YYYY-MM-DD"),

});

//buscar tipo de gasto
$('select[name="tipo_gasto"]').select2({
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
        },
    allowClear: true,
    ajax: {
        delay: 250,
        type: 'POST',
        url: window.location.pathname,
        data: function (params) {
            return {
                term: params.term,
                action: 'search_tipo_gasto'
            };
        },
        processResults: function (data) {
            console.log(data);
            return {
                results: data
            };
        },
    },
    placeholder: 'Ingrese una descripción',
    minimumInputLength: 1,
});

})
;