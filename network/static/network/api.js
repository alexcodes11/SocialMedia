
function updatelike(like) {
  fetch(`/updatelike/${like}`)
    .then((response) => response.text())
    .then((count) => {
      console.log(count);
      document.querySelector(`li[data-id="${like}6"]`).innerHTML = count;
     
    });
}

function editpost(edit){
  fetch(`/editpost/${edit}`)
    .then(response => response.json())
    
    .then(post => {
      //  document.querySelector(`li[data-id="${edit}"]`).innerHTML = ` PLEASE: ${data}`;
      var mainContainer = document.querySelector(`li[data-id="${edit}"]`);
      mainContainer.style.display = "none";
      for (var i = 0; i < post.length; i++) {
        var textarea = document.querySelector(`textarea[data-id="${edit}2"]`)
        textarea.style.display = "block"
        textarea.innerHTML = post[i].post; 
        document.querySelector(`button[data-id="${edit}3"]`).style.display = "block"
        document.querySelector(`button[data-id="${edit}4"]`).style.display = "block"
      }
    })

}

function cancel(){
  location.reload();
}

function edit(id){

 var textarea = document.querySelector(`textarea[data-id="${id}2"]`).value;

 fetch(`/edit/${id}/${textarea}`)
   .then((response) => response.text())
   .then((result) => {
     document.querySelector(`button[data-id="${id}3"]`).style.display = "none"
     document.querySelector(`button[data-id="${id}4"]`).style.display = "none"
     document.querySelector(`textarea[data-id="${id}2"]`).style.display = "none";
     document.querySelector(`li[data-id="${id}"]`).innerHTML = textarea;
     document.querySelector(`li[data-id="${id}"]`).style.display = "block";

   });
  };
