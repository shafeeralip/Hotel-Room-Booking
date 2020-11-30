







var room_selected=document.getElementsByClassName("roomselect")
console.log("room",room_selected)
// roomprice=new Array()
// selceted_value=new Array()
var guest=document.getElementById("adults")
var checkin=document.getElementById("checkin") 
var checkout=document.getElementById("checkout")
var message=document.getElementById("message")



for(var i=0;i<room_selected.length;i++){

    room_selected[i].addEventListener('change',function(){
           
        if(checkin.value && checkout.value && guest.value){
            
            
            console.log("date",checkin.value)
          
            
            checkindate=new Date(checkin.value)
            checkoutdate=new Date(checkout.value) 

            console.log("hello",checkindate)
            var diffdate=(checkoutdate-checkindate)
            var diffDays =(diffdate / 1000 / 60 / 60 / 24);

            document.getElementById("totalDays").textContent=diffDays

            var peoples=parseInt(guest.value)
            
            if(peoples % 2 ==0){
                
                var person_allowed=peoples/2  
            }
            else{
                var people=peoples +1
                var person_allowed=people/2
            }
            
            var totalrooms = 0
            var room_price=new Array()
            var dict=[];

            
      
            

            document.querySelectorAll('.priceroom').forEach(ele=>{
                console.log("helloo",ele.textContent);
                room_price.push(ele.textContent)

            })
            k=0
            document.querySelectorAll('.roomselect').forEach(ele=>{
               
                totalrooms=totalrooms +parseInt(ele.value) 
                dict.push({
                    roomprice:room_price[k],
                    roomscount:ele.value
                    
                });
  
                k++
            })

            if(totalrooms < person_allowed ){
               var person_room_want= peoples - ( 2 * totalrooms) 
                document.getElementById('messageinput').innerHTML='you still need to fit  '+ person_room_want +'  more adults'
               message.style.display='block'
               
               
            }
            else{
                message.style.display='none'
            }

           
    
           
           document.getElementById("roomscount").textContent=totalrooms
           var totalprice=0
            for(i=0;i<dict.length;i++){
                console.log("roomprice",dict[i].roomprice,'roomscount',dict[i].roomscount)
                totalprice=totalprice +(parseInt(dict[i].roomprice) * parseInt(dict[i].roomscount)) *diffDays
            }
            
            document.getElementById('roomsprice').textContent=totalprice


        }
        else{
            alert('Please Fill FIRST  '+toUnicodeVariant('CHECKIN ,CHECKOUT AND GUEST', 'bold sans', 'underline')+' VALUE');
            
        }

            
    })


}

window.mytest=function(){
    var totalprice=document.getElementById('roomsprice').textContent
    var checkintime=checkin.value
    var checkouttime=checkout.value
    var totalguest=document.getElementById("adults").value
    

    room_detail=[]
    
    document.querySelectorAll('.roomselect').forEach(ele=>{
        // console.log(ele.dataset.roomid)
        room_detail.push({
            roomid:ele.dataset.roomid,
            roomscount:ele.value,
            hotelid:ele.dataset.hotelid,
            totalprice:totalprice,
            checkin:checkintime,
            checkout:checkouttime,
            totalguest:totalguest

        });
    })

    var url='/booking_details/'

    fetch(url, {
            method:'POST',
            headers:{'X-CSRFToken':csrftoken,
                'Content-Type':'application/json',
     
            },
            body:JSON.stringify({'room_detail':room_detail})
        })
        .then((response) =>{
            return response.json()
        })
        .then((data)=>{
            console.log('data :',data)
            document.getElementById("continue").type='submit'
            document.getElementById("vj").style.display='none'
          
         
         })

   
    
}