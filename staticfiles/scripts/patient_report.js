function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll(".section").forEach((section) => {
    section.classList.remove("active");
  });
  // Show the selected section
  document.getElementById(sectionId).classList.add("active");
  // Update active tab
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  event.target.classList.add("active");
}
