const body = document.querySelector("body"),
      modeToggle = body.querySelector(".mode-toggle");
      sidebar = body.querySelector("nav");
      sidebarToggle = body.querySelector(".sidebar-toggle");
      profilepic=body.querySelector(".profilepic");
      card=body.querySelector(".card");

let getMode = localStorage.getItem("mode");
if(getMode && getMode ==="dark"){
    body.classList.toggle("dark");
}

let getStatus = localStorage.getItem("status");
if(getStatus && getStatus ==="close"){
    sidebar.classList.toggle("close");
}

modeToggle.addEventListener("click", () =>{
    body.classList.toggle("dark");
    if(body.classList.contains("dark")){
        localStorage.setItem("mode", "dark");
    }else{
        localStorage.setItem("mode", "light");
    }
});

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    if(sidebar.classList.contains("close")){
        localStorage.setItem("status", "close");
    }else{
        localStorage.setItem("status", "open");
    }
})

profilepic.addEventListener("click", () => {
    if(card.style.display=='none'){
        card.style.display='block';
    }
    else{
        card.style.display='none'
    }
    
})


 // When the user clicks on <div>, open the popup
 function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
  }
  function openEditProfile(){
      window.location.href='FacultyEditProfile.html';

  }
 


// files adding removing


                function uploadanother(elem)
                {
                var document    = $(elem).parent().prev().find('input[type="file"]').val();
                if(document!='')
                {
                var clonewrap   = $(elem).parent().parent().clone();                
                clonewrap.find('button').removeAttr('onclick');
                clonewrap.find('button').attr('onclick','removeupload(this)');
                clonewrap.find('button').html('Delete');
                $(elem).parent().parent().before(clonewrap);
                $(elem).parent().prev().find('input[type="file"]').val('');
                }
                else{
                   
                    error.textContent = "Please upload file"
                     error.style.color = "red"
                    uploadfile.style.borderColor = 'red'
                    uploadfile.style.borderColor = 'red'
                    uploadfile.style.borderStyle = 'solid'

                }
                }
                
                function removeupload(elem)
                {
                $(elem).parent().parent().remove();
                }