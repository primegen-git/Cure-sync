function showSection(sectionId, element) {
  // Hide all tab content panes
  const tabPanes = document.querySelectorAll(".tab-pane");
  tabPanes.forEach((pane) => {
    pane.classList.remove("active");
  });

  // Deactivate all tab navigation items
  const tabItems = document.querySelectorAll(".tab-item");
  tabItems.forEach((item) => {
    item.classList.remove("active");
  });

  // Show the selected tab content pane
  const selectedPane = document.getElementById(sectionId);
  if (selectedPane) {
    selectedPane.classList.add("active");
  }

  // Activate the clicked tab navigation item
  if (element) {
    element.classList.add("active");
  }
}
