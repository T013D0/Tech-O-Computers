$(document).ready(() => {
  if (user === "AnonymousUser") {
    $(".update-cart").hide();
    $(".not-logged").show();
  } else {
    $(".update-cart").show();
    $(".not-logged").hide();
  }
  $(".update-cart").click((e) => {
    const buy = e.target.dataset.buy || e.currentTarget.dataset.buy;
    const productId =
      e.target.dataset.product || e.currentTarget.dataset.product;
    const action = e.target.dataset.action || e.currentTarget.dataset.action;
    if (user === "AnonymousUser") {
      return;
    } else {
      updateUserOrder(productId, action, buy === "true");
    }
  });
});

function updateUserOrder(productId, action, buy = false) {
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
      if (buy) {
        window.location.href = "/shipping-cart/";
        return;
      }
      location.reload();
    });
}
