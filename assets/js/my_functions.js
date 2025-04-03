function alert_ajax_error(){
    swal({
        title: 'Salesintel',
        text: 'Unable to get response from server, please check your internet connection.',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#fff',
        confirmButtonText: 'Yes!',
        cancelButtonText: 'No.',

    });

}
function active_spinner(){
    $(".myloader").addClass("active");
    $("body").addClass("blurry");
}
function remove_spinner(){
    $(".myloader").removeClass("active");
    $("body").removeClass("blurry");
}