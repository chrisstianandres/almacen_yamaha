var datatable;
$(function () {
    datatable = $('#example1').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        }
    });

    $('#example1 tbody')
        .on('click', 'a[rel="del"]', function (){
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data[0]};
        parametros['action'] = 'delete';
        submit_with_ajax_other('/cargo/eliminar/'+data[0]+'/', 'Alerta de Eliminacion!',
            'Esta seguro que desea borrar este cargo', parametros, function (){
            window.location.reload();
            })
    })
});