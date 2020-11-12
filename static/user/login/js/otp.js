
var verify=document.getElementById('verify')

verify.addEventListener('click',function(e){
    
    console.log('clicked')
   
    var pattern= /^[6-9]{1}[0-9]{9}$/;

    var mobile=document.getElementById("mobile_reg").value
    if(mobile){
        document.getElementById("otp").setAttribute('type','text'); 

        var url='/otp_generate'

        fetch(url, {
            method:'POST',
            headers:{'X-CSRFToken':csrftoken,
                'Content-Type':'application/json',
     
            },
            body:JSON.stringify({'mobile':mobile})
        })
        .then((response) =>{
            return response.json()
        })
        .then((data)=>{
            console.log('data :',data)
         //    location.reload()
         })





    }

   



    

})