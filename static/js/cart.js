$(document).ready(() => {
  if (user === "AnonymousUser") {
    $(".update-cart").hide();
    $(".not-logged").show();
  } else {
    $(".update-cart").show();
    $(".not-logged").hide();
  }
  $(".update-cart").click((e) => {
    console.log(e);
    const productId =
      e.target.dataset.product || e.currentTarget.dataset.product;
    const action = e.target.dataset.action || e.currentTarget.dataset.action;
    if (user === "AnonymousUser") {
      return;
    } else {
      updateUserOrder(productId, action);
    }
  });
});

function updateUserOrder(productId, action) {
  const url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId, action }),
  })
    .then((response) => response.json())
    .then((data) => {
      location.reload();
    });
}
