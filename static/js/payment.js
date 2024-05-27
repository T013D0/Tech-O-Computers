async function sendPayment(amount) {
  fetch("/webpay-plus-create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ amount: amount }),
  })
    .then((response) => {
      console.log("Response Status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Response Data:", data);
      if (data.url) {
        // Crear y enviar el formulario automáticamente
        const form = document.createElement("form");
        form.method = "post";
        form.action = data.url;
        form.name = "form_pay";

        const tokenInput = document.createElement("input");
        tokenInput.type = "hidden";
        tokenInput.name = "token_ws";
        tokenInput.value = data.token;

        const amountInput = document.createElement("input");
        amountInput.type = "hidden";
        amountInput.name = "amount";
        amountInput.value = amount;

        form.appendChild(tokenInput);
        form.appendChild(amountInput);
        document.body.appendChild(form);

        // Redirigir automáticamente
        const body = document.createElement("body");
        body.setAttribute("onload", "document.form_pay.submit()");
        body.appendChild(form);
        document.body.appendChild(body);
        document.form_pay.submit();
      } else {
        console.error("Error:", data.error);
        alert("Error al iniciar el pago: " + data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}
$(document).ready(() => {
  let formSubmitted = false;

  $("#shippingForm").submit(async (event) => {
    event.preventDefault();

    if (formSubmitted) return; // prevent multiple submissions

    formSubmitted = true;

    const amount = total;

    const address = $("#address").val();
    const city = $("#city").val();
    const state = $("#state").val();
    const country = $("#country").val();
    const postal_code = $("#zip").val();
    const comments = $("#comments").val();

    fetch("/shipping/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        address: address,
        city: city,
        state: state,
        country: country,
        postal_code: postal_code,
        comments: comments,
      }),
    })
      .then((response) => {
        console.log("Response Status:", response.status);
        return response.json();
      })
      .then((data) => {
        console.log("Response Data:", data);
        if (data.success) {
          sendPayment(amount);
        } else {
          console.error("Error:", data.error);
          alert("Error al guardar la dirección de envío: " + data.error);
        }
      });
  });
});
