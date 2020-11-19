var room_selected=document.getElementsByClassName("roomselect")
console.log("room",room_selected)
// roomprice=new Array()
// selceted_value=new Array()

for(var i=0;i<room_selected.length;i++){
    

    console.log("length",room_selected.length)

    room_selected[i].addEventListener('change',function(){

            var totalrooms = 0
            var room_price=new Array()
            var dict=[];
            console.log("helloll",i)
      
            

            document.querySelectorAll('.priceroom').forEach(ele=>{
                console.log("helloo",ele.textContent);
                room_price.push(ele.textContent)



            })
            k=0
            document.querySelectorAll('.roomselect').forEach(ele=>{
                console.log("helloo",ele.value);
                totalrooms=totalrooms +parseInt(ele.value) 
                dict.push({
                    roomprice:room_price[k],
                    roomscount:ele.value
                    
                });
  
                k++

            })
           
        console.log("dic:",dict)
           console.log("total rooms:",totalrooms)
           document.getElementById("roomscount").textContent=totalrooms
           var totalprice=0
            for(i=0;i<dict.length;i++){
                console.log("roomprice",dict[i].roomprice,'roomscount',dict[i].roomscount)
                totalprice=totalprice +(parseInt(dict[i].roomprice) * parseInt(dict[i].roomscount))
            }
            console.log('totalprice',totalprice)
            document.getElementById('roomsprice').textContent=totalprice


    })


}