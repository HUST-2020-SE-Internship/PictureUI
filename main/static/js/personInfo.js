function showImg(){
    var file =  document.getElementById('upfile').files[0];
    var pic=document.getElementById('imgshow');
    var re = new FileReader();
    re.readAsDataURL(file);
    re.onload = function(re){
    	console.log(re);
        pic.src=re.target.result;
    }
}

function load(){
	var file =  document.getElementById('upfile').files[0];
	var nickName = document.getElementById('nickName').value;
	var telephone = document.getElementById('telephone').value;
	var user_id = document.getElementById('user_id').value;
	var re = new FileReader()
	var url = "/main/account/" + user_id + "/personInfo/"
	if (file != null){
		re.readAsDataURL(file);
		re.onload = function(re){
				var image = re.target.result ;
				$.ajax({
				url: url ,
				type: "POST",
				data: {
					nickName: nickName,
					telephone:telephone,
					image: JSON.stringify(image),
				},
				beforeSend: function(xhr, settings){
					xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
				},
				success: result => {
					console.log("success ") ;
				}
			})
			}
	}else {
		$.ajax({
				url: url ,
				type: "POST",
				data: {
					nickName: nickName,
					telephone:telephone,
				},
				beforeSend: function(xhr, settings){
					xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
				},
				success: result => {
					console.log("success ") ;
				}
			})
	}

}


function upLoadPic() {
    var dir=document.getElementById("upfile");
    dir.click();
}