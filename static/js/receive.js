$(document).ready(function(){
    function receive()
    {
        $.ajax({
            url:'/arduino/receivedum',
            method:'post', 
            data:{},
            success:function(data){
                // console.log(data);
                if (data == "success") {
                    $toast("Message received!", "#018401");
                    toastr.success("Message received!");
                }
                if (data == "error") {
                    $toast("SIM900 Module is not working properly. Please setup again.", "#dc3545");
                    toastr.danger("SIM900 Module is not working properly. Please setup again.");
                }
            }
        })
    }

    setInterval(receive, 1000);
})