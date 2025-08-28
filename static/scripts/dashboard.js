document.addEventListener("DOMContentLoaded", function () {
  const navItems = document.querySelectorAll("nav ul li");
  navItems.forEach((item) => {
    item.setAttribute("tabindex", "0");
    item.setAttribute("role", "menuitem");
    item.addEventListener("click", function () {
      navItems.forEach((nav) => nav.classList.remove("active"));
      this.classList.add("active");
    });
    item.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        navItems.forEach((nav) => nav.classList.remove("active"));
        this.classList.add("active");
      }
    });
  });
});
