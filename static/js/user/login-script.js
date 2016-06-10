function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var user = getCookie("username");
    if (user != "") {
        alert("Welcome again " + user);
    }
}
$(function(){
	$('button').click(function(){
		var user = $('#txtUsername').val();
		var pass = $('#txtPassword').val();
		$.ajax({
			url: '/logInUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				var jsonResponseData = JSON.parse(response);
				var status = jsonResponseData["status"]
				var token = jsonResponseData["token"]
				if (status) {
				    setCookie("username", user, 1)
				    setCookie("token", token, 1)
				    history.go(-1);
				}
				else {
				    alert("Please login again");
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
