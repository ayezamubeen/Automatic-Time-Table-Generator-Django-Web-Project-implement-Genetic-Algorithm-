// When the user clicks on <div>, open the popup
function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}
function showform(){
    document.getElementById('add_form').style.display = "flex";
}
function show_edit_form(a){
  var form = document.getElementsByClassName('edit_form')[a-1];
  form.style.display = 'flex';
}
function show_mail_form(a){
  var form = document.getElementsByClassName('mail_form')[a-1];
  form.style.display = 'flex';
}

