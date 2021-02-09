$(document).ready(function(){
    function receive()
    {
        $.ajax({
            url:'/arduino/receivedum',
            method:'post', 
            data:{},
            success:function(data){
                // console.log(data);
            }
        })
    }

    setInterval(receive, 1000);
})