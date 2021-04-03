function handleHelpTitleClick(btn) {
  let response = btn.nextElementSibling;
  btn.classList.toggle("open");
  if (response.style.maxHeight) {
    response.style.maxHeight = null;
  } else {
    response.style.maxHeight = response.scrollHeight + "px";
  }
}
