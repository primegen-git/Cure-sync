document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("online_request");
  button.addEventListener("click", function () {
    const my_url = this.getAttribute("data-url");
    window.location.href = my_url;
  });
});
