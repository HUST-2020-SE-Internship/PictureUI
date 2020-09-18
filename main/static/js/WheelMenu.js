/* 轮盘菜单使用 */
/* Dependency: GalMenu.js */
var items = document.querySelectorAll('.menuItem');
for (var i = 0,l = items.length; i < l; i++) {
    items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";
    items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%"
}
var index=0;
var scrollFunc = function (e) {
    index=index%6;
    e = e || window.event;
    if (e.wheelDelta) { //第一步：先判断浏览器IE，谷歌滑轮事件    
        if (e.wheelDelta > 50) { //当滑轮向上滚动时 
            index++;
            if(index>0){
                for (var i = 0,l = items.length; i < l; i++) {
                    if(i==items.length-1){
                        items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (0+index-1) * Math.PI)).toFixed(4) + "%";
                        items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (0+index-1) * Math.PI)).toFixed(4) + "%";
                    }else{
                        console.log(i+index);
                        items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                        items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                    }
                }
            }else{
                for (var i = 0,l = items.length; i < l; i++) {
                    if(i+index<0){
                        items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (l+i+index) * Math.PI)).toFixed(4) + "%";
                        items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (l+i+index) * Math.PI)).toFixed(4) + "%";
                    }else{
                        console.log(i+index);
                        items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                        items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                    }
                }
            }	
        }
    }
        if(e.wheelDelta < 50) { //当滑轮向下滚动时 
            index--;
            if(index>0){
                for (var i = 0,l = items.length; i < l; i++) {
                if(i==items.length-1){
                    items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (0+index-1) * Math.PI)).toFixed(4) + "%";
                    items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (0+index-1) * Math.PI)).toFixed(4) + "%";
                }else{
                    console.log(i+index);
                    items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                    items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                }
                
                }
            }else{
                for (var i = 0,l = items.length; i < l; i++) {
                if(i+index<0){
                    items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (l+i+index) * Math.PI)).toFixed(4) + "%";
                    items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (l+i+index) * Math.PI)).toFixed(4) + "%";
                }else{
                    console.log(i+index);
                    items[i].style.left = (50 - 35 * Math.cos( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                    items[i].style.top = (50 + 35 * Math.sin( - 0.5 * Math.PI - 2 * (1 / l) * (i+index) * Math.PI)).toFixed(4) + "%";
                }
                
                }
            }
    } else if (e.detail) { //Firefox滑轮事件 
        if (e.detail > 50) { //当滑轮向上滚动时 
            console.log("滑轮向上滚动fx");
        }
        if (e.detail < 50) { //当滑轮向下滚动时 
            console.log("滑轮向下滚动fx");
        }
    }	
}  

var scrollRotate=document.getElementById("overlay");
if (scrollRotate.addEventListener) {//firefox 
    scrollRotate.addEventListener('DOMMouseScroll', scrollFunc, false);
}        
//滚动滑轮触发scrollFunc方法 //ie 谷歌 
window.onmousewheel = scrollRotate.onmousewheel ;
scrollRotate.onmousewheel = scrollFunc;