$(document).ready(() => {
  $("#delivery").change(async () => {
    const status = $("#delivery").val();

    fetch(`/api/order/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ id, status }),
    }).then((response) => {
      if (response.ok) {
        if (response.status === 200) {
          location.reload();
        } else {
          $("#statusError").show();
        }
      }
    });
  });
});
