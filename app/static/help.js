function handleHelpTitleClick(elem) {
    let content = elem.nextElementSibling;
    if(content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight+"px";
    }
  }