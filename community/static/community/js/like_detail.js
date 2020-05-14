const likeBtn = document.querySelector(".js-like");

const toggleLike = async (event) => {
  const btn = event.target;
  const likeCntSpan = btn.previousElementSibling.querySelector(
    "span"
  );
  const currCnt = Number(likeCntSpan.innerText);
  const article =
    btn.parentElement.parentElement.parentElement;
  const article_pk = window.location.href
    .split("/community/")[1]
    .replace("/", "");
  const url = `/community/${article_pk}/like/`;
  const csrfToken = document.cookie
    .split("; ")
    .filter((str) => str.includes("csrftoken"))[0]
    .split("=")[1];

  const data = await fetch(url, {
    credentials: "include",
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((res) => res.json())
    .catch((err) => console.log(err));

  const newCnt = Number(data["cnt"]);

  if (typeof newCnt !== "undefined") {
    likeCntSpan.innerText = newCnt;
    if (newCnt + 1 === currCnt) {
      btn.innerText = "좋아요";
    } else if (currCnt + 1 === newCnt) {
      btn.innerText = "좋아요 취소";
    }
  }
};

likeBtn.addEventListener("click", toggleLike);
