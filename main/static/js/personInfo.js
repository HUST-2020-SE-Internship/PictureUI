function showImg(){
    var file =  document.getElementById('upfile').files[0];
    var pic=document.getElementById('imgshow');
    var re = new FileReader();
    re.readAsDataURL(file);
    re.onload = function(re){
        pic.src=re.target.result;
    }
}

document.getElementById("upfile").addEventListener("change",function(event){
    let files = event.target.files;
    if(files.length != 0){
        //上传文件夹，这里得到的该文件夹下所有的文件，取第0个，得到文件夹名字即可
        console.log(files);
        var s = files[0].webkitRelativePath;
        console.log(s);
        var str = s.split("/") ;
        console.log(str);
        var fileName = str[0];
        console.log(fileName);
        //这里可以写ajax请求，把文件夹名字fileName带过去就可以，我在这一块就不写了
    }
},false);

function upLoadPic() {
    var dir=document.getElementById("upfile");
    dir.click();
}