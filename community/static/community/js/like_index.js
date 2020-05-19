const likeBtns = document.querySelectorAll(".js-like");

const changeTemplate = function (target, { liked, count }) {
  if (liked) {
    target.innerText = "좋아요 취소";
  } else {
    target.innerText = "좋아요";
  }

  const id = target.dataset.id;
  const countSpan = document.querySelector(
    `#like-count-${id}`
  );
  countSpan.innerText = count;
};

const toggleLike = function ({ target }) {
  const id = target.dataset.id;
  const URL = `/community/${id}/like/`;
  const csrfToken = document.cookie
    .split("; ")
    .filter((str) => str.includes("csrftoken"))[0]
    .split("=")[1];

  fetch(URL, {
    credentials: "include",
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((res) => res.json())
    .then((data) => changeTemplate(target, data));
};

if (likeBtns) {
  likeBtns.forEach((likeBtn) =>
    likeBtn.addEventListener("click", toggleLike)
  );
}
