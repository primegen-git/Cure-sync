document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("profile");
  if (button) {
    button.setAttribute("tabindex", "0");
    button.setAttribute("role", "button");
    button.addEventListener("click", function () {
      const my_url = this.getAttribute("data-url");
      window.location.href = my_url;
    });
    button.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        const my_url = this.getAttribute("data-url");
        window.location.href = my_url;
      }
    });
  }
});
