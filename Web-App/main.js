document.getElementById('submiter').addEventListener('click', function(event) {
    event.preventDefault();
    if($('#nom').val()==""){
        $('#nom').attr('style',"border:2px solid red");
    } else {
        $('#nom').attr('style',"border:1px solid gray");
    }
    if($('#prenom').val()==""){
        $('#prenom').attr('style',"border:2px solid red");
    } else {
        $('#prenom').attr('style',"border:1px solid gray");
    }
    if($('#courriel').val()==""){
        $('#courriel').attr('style',"border:2px solid red");
    } else {
        $('#courriel').attr('style',"border:1px solid gray");
    }
    if($('#courriel').val()!="" && $('#nom').val() !== "" && $('#prenom').val() !== ""){
        localStorage.setItem('nom', $('#nom').val());
        localStorage.setItem('prenom', $('#prenom').val());
        localStorage.setItem('courriel', $('#courriel').val());
        window.location.href = "./welcome.html"; 
    }
});

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        $('#blah').attr('src', e.target.result);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
}
function getLocation() {
    if(document.getElementById("select").files.length > 0){
            navigator.geolocation.getCurrentPosition((position)=> {
            const p=position.coords;
            localStorage.setItem('lat', p.latitude);
            localStorage.setItem('long', p.longitude);
            sendRequest();
        })
    }
}

function checkForm(){
    if (localStorage.getItem("nom")!="" && localStorage.getItem("prenom")!=""&&localStorage.getItem("courriel")!=""){
        window.location.href = "welcome.html"
    }
}

function sendRequest() {
    const formData = new FormData();
    formData.append('file', document.getElementById("select").files[document.getElementById("select").files.length - 1]);
    formData.append('lat', localStorage.getItem("lat"));
    formData.append('lon', localStorage.getItem("long"));
    formData.append('nom', localStorage.getItem("nom"));
    formData.append('prenom', localStorage.getItem("prenom"));
    formData.append('courriel', localStorage.getItem("courriel"));
    formData.append('description', localStorage.getItem("description"));
    
    try {
        fetch(window.origin+'/upload-file/', {
            method: 'POST',
            body: formData
        }).then((response) => {
            console.log(response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = response.json();
            window.location.href = "merci.html"
        });
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
}