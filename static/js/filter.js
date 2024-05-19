$(document).ready(() => {
  $("#orderBy").change(() => {
    const orderBy = $("#orderBy").val();
    let url = window.location.href;
    let newUrl = url.split("?")[0];
    if (url.includes("?")) {
      const params = url.split("?")[1].split("&");
      let newParams = [];
      for (let i = 0; i < params.length; i++) {
        if (params[i].includes("orderBy")) {
          continue;
        }
        newParams.push(params[i]);
      }
      newParams.push("orderBy=" + orderBy);
      newUrl += "?" + newParams.join("&");
    } else {
      newUrl += "?orderBy=" + orderBy;
    }
    window.location.href = newUrl;
  });
});
