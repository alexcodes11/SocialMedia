function updatelike(like) {
  fetch(`/updatelike/${like}`)
    .then((response) => response.json())
    .then((like) => {
      console.log(like);
    });
}
