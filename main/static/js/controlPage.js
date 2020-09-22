var index=0;
function showhide() {
    var div = document.getElementById("newpost");
    if (div.style.display !== "none") {
        div.style.display = "none";
    } else {
        div.style.display = "block";
    }
}

function changePage(obj){
    index=obj.innerText-1;
    var nowPage;
    var itemList=document.querySelectorAll(".item");
    for(let i=0;i< itemList.length;i++){
        if(itemList[i].style.display!="none"){
             nowPage=i;
        }
    }
    if(obj.innerText=="next"&&nowPage!=itemList.length-1){
        index=nowPage+1;
    }else if (obj.innerText=="next"&&nowPage==itemList.length-1){
        index=0;
    }

    if(obj.innerText=="prev"&&nowPage!=0){
        index=nowPage-1;
    }else if (obj.innerText=="prev"&&nowPage==0){
        index=itemList.length-1;
    }

    itemList[nowPage].style.animation="action_scaleOut 0.5s"
    setTimeout(function (){
        itemList[nowPage].style.display="none";
        itemList[nowPage].style.opacity=0;
        itemList[index].style.display="block";
        itemList[index].style.opacity=1;
        itemList[index].style.animation="action_scale 2s";
    },500);
}