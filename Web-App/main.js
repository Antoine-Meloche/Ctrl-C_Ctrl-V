//-------------------------------------------
//   Code for the initial form
//-------------------------------------------

// Function to save data from the initial form
document.getElementById('submiter').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent form submission

    // Validate form fields (fields become red if empty)
    if ($('#nom').val() == "") {
        $('#nom').css('border', '2px solid red');
    } else {
        $('#nom').css('border', '1px solid gray');
    }
    if ($('#prenom').val() == "") {
        $('#prenom').css('border', '2px solid red');
    } else {
        $('#prenom').css('border', '1px solid gray');
    }
    if ($('#courriel').val() == "") {
        $('#courriel').css('border', '2px solid red');
    } else {
        $('#courriel').css('border', '1px solid gray');
    }

    // Save data if all fields are filled
    if ($('#courriel').val() != "" && $('#nom').val() !== "" && $('#prenom').val() !== "") {
        localStorage.setItem('nom', $('#nom').val());
        localStorage.setItem('prenom', $('#prenom').val());
        localStorage.setItem('courriel', $('#courriel').val());
        // Redirect to the main page
        window.location.href = "./welcome.html";
    }
});

// Function to check if form data already exists
function checkForm() {
    console.log(localStorage.getItem("nom"))
    if (localStorage.getItem("nom") != null && localStorage.getItem("prenom") != null && localStorage.getItem("courriel") != null) {
        window.location.href = "welcome.html"
    }
}

//-------------------------------------------
//   Code for the description form
//-------------------------------------------

function idgaf() {
    event.preventDefault(); // Prevent form submission

    // Validate textarea (becomes red if empty)
    if ($('textarea').val() == "") {
        $('textarea').css('border', '2px solid red');
    }

    // Save data if textarea is not empty
    if ($('textarea').val() != "") {
        localStorage.setItem('description', $('textarea').val());
        // Redirect to the camera page
        window.location.href = "./camera.html";
    }
}

//-------------------------------------------
//   Code to send photo and data
//-------------------------------------------

// Function to display the selected photo
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Function to get location and send data
function getLocation() {
    if (document.getElementById("select").files.length > 0) {
        document.getElementById("snap").style.outline = "3px solid white";
        navigator.geolocation.getCurrentPosition((position) => {
            const p = position.coords;
            localStorage.setItem('lat', p.latitude);
            localStorage.setItem('long', p.longitude);
            sendRequest(); // Start sending data
        })
    } else {
        // Button becomes red if no photo is selected
        document.getElementById("snap").style.outline = "2px solid red";
    }
}

// Function to send data
function sendRequest() {
    const formData = new FormData();

    // Collect data
    formData.append('file', document.getElementById("select").files[document.getElementById("select").files.length - 1]);
    formData.append('lat', localStorage.getItem("lat"));
    formData.append('lon', localStorage.getItem("long"));
    formData.append('nom', localStorage.getItem("nom"));
    formData.append('prenom', localStorage.getItem("prenom"));
    formData.append('courriel', localStorage.getItem("courriel"));
    formData.append('description', localStorage.getItem("description"));

    // Send data
    try {
        fetch(window.origin + '/upload-file/', {
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
