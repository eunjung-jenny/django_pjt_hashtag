add_child_comment_btns = document.querySelectorAll(
  ".js-add-child-comment"
);

function handeler(event) {
  comment_container =
    event.target.parentNode.parentNode.parentNode;
  child_comment_form = comment_container.querySelector(
    ".js-child-comment-form"
  );
  console.log(child_comment_form);
  if (child_comment_form.classList.contains("show")) {
    child_comment_form.classList.remove("show");
  } else {
    child_comment_form.classList.add("show");
  }
}

function init() {
  add_child_comment_btns.forEach((btn) =>
    btn.addEventListener("click", handeler)
  );
}

init();

// ".add-child-comment"
