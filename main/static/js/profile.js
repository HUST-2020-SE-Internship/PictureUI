document.getElementById("upfile").addEventListener("change",function(event){
    var files=event.target.files;
    if(files.length != 0){
        //上传文件夹，这里得到的该文件夹下所有的文件，取第0个，得到文件夹名字即可
        var re = new FileReader();
        re.readAsDataURL(files[0]);
        re.onload = function(re){
            console.log(re.target.result);
        }
        var s = files[0].webkitRelativePath;
        var str = s.split("/") ;
        var fileName = str[0];
        var showFile=document.getElementById("showfiles");
        showFile.innerHTML+=`<div style="text-align: center"><img src="/static/mainstatic/文件夹.png" width="50px" height="50px"/><div>${fileName}</div></div>`;
        //这里可以写ajax请求，把文件夹名字fileName带过去就可以，我在这一块就不写了
    }
},false);


function showPic() {
    var file =  document.getElementById('upfile2').files[0];
    console.log(file);
    var re = new FileReader();
    re.readAsDataURL(file);
    re.onload = function(re){
        console.log(re.target.result);
        var showFile=document.getElementById("showfiles");
        showFile.innerHTML+=`<div style="text-align: center"><img src=${re.target.result} width="50px" height="50px"/><div>${file.name}</div></div>`;
    }

}

function upLoadPic(id) {
    var dir=document.getElementById(id);
    dir.click();
}

function upLoadPicture() {
    window.location.reload();
}