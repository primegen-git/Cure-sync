document.addEventListener("DOMContentLoaded", function () {
  // Select all list items within the nav
  const navItems = document.querySelectorAll("nav ul li");

  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Remove 'active' class from all items
      navItems.forEach((nav) => nav.classList.remove("active"));

      // Add 'active' class to the clicked item
      this.classList.add("active");
    });
  });
});
