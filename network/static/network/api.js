
function updatelike(like) {
  fetch(`/updatelike/${like}`)
    .then((response) => response.json())
    .then((count) => {
      console.log(count);
      document.querySelector(`span[data-id="${like}6"]`).innerHTML = count['count'];
       var element = document.querySelector(`a[data-id="${like}7"]`);
      if (element.className === "liked"){
        element.className = "unlike";
      }
      else if (element.className === "unlike"){
        element.className = "liked"
      }
      else{
        element.className = `${count["liked"]}`
      }
    });
}

function editpost(edit){
  fetch(`/editpost/${edit}`)
    .then(response => response.json())
    
    .then(post => {
      //  document.querySelector(`li[data-id="${edit}"]`).innerHTML = ` PLEASE: ${data}`;
      var mainContainer = document.querySelector(`p[data-id="${edit}"]`);
      mainContainer.style.display = "none";
      for (var i = 0; i < post.length; i++) {
        var textarea = document.querySelector(`textarea[data-id="${edit}2"]`)
        textarea.style.display = "block"
        textarea.innerHTML = post[i].post; 
        document.querySelector(`a[data-id="${edit}3"]`).style.display = "block"
        document.querySelector(`a[data-id="${edit}4"]`).style.display = "block"
        document.querySelector(`a[data-id="${edit}7"]`).style.display = "none";
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
     document.querySelector(`a[data-id="${id}3"]`).style.display = "none"
     document.querySelector(`a[data-id="${id}4"]`).style.display = "none"
     document.querySelector(`textarea[data-id="${id}2"]`).style.display = "none";
     document.querySelector(`p[data-id="${id}"]`).innerHTML = textarea;
     document.querySelector(`p[data-id="${id}"]`).style.display = "block";
     document.querySelector(`a[data-id="${id}7"]`).style.display = "block";

   });
  };
