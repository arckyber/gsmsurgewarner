$(document).ready(function() {
	function arduinoRender() {
		$.ajax({
			url:'/arduino/render',
			data:{},
			method:'POST',
			success:function(data) {
				if (data.connected == true) {
					$("#footerTextColor").removeClass("text-danger");
					$("#footerTextColor").addClass("text-primary");
					$("#footerMessage").text("Connected");
				}
				else {
					$("#footerTextColor").removeClass("text-primary");
					$("#footerTextColor").addClass("text-danger");
					$("#footerMessage").text("Reciever not detected!");
				}
				console.log(data);
			}
		})
	}

	// setInterval(arduinoRender, 1000);
})
