document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("profile");
  button.addEventListener("click", function () {
    const my_url = this.getAttribute("data-url");
    window.location.href = my_url;
  });
});
