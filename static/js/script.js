function getname(data){
    var a = data;
    localStorage.setItem("title", a);
    localStorage.setItem("title1", a);
}
function getIsbn(n){
    localStorage.setItem("isbn",n);
    document.getElementById("submit").click();
}
function validate1() {
  var x = document.forms["bksearch"]["isbn"].value;
  var y = document.forms["bksearch"]["title"].value;
  var z = document.forms["bksearch"]["author"].value;
  if (x == "" && y == "" && z == ""){
    alert("Please enter atleast one info of book");
    return false;
  }
}
function validate2() {
  var txt = document.forms["review_form"]["review"].value;
  if (txt == ""){
    alert("Error! Review cannot be blank");
    return false;
  }
}
window.addEventListener('load', (event) => {
    document.getElementById("result").value = localStorage.getItem("title");
    document.getElementById("result1").value = localStorage.getItem("title1");
    document.getElementById("isbn").value = localStorage.getItem("isbn");
});