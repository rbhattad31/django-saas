$(document).ready(function () {
  var currentPath = window.location.pathname;
  console.log("Current path:", currentPath);

  // ✅ Handle submenu links
  $(".list-group-item a").each(function () {
    let href = this.getAttribute("href");

    
    console.log(currentPath.startsWith(href))

    if (href && currentPath.startsWith(href)) {
      // Add active to submenu <li>
      $(this).parent("li").addClass("active");

      // Expand parent submenu
      let parentCollapse = $(this).closest(".collapse");
      parentCollapse.addClass("show");

      // Add active to parent <li> (main menu)
      parentCollapse.closest(".nav-item").addClass("active");
    }
  });

  // ✅ Handle top-level nav links (no submenu)
  $(".nav-item > .nav-link").each(function () {
    let href = this.getAttribute("href");

    if (href && currentPath.startsWith(href)) {
      $(this).addClass("active");
      $(this).parent(".nav-item").addClass("active");
    }
  });

  // ✅ Accordion behavior: only one open at a time
  $(".nav-link[data-bs-toggle='collapse']").on("click", function () {
    let target = $(this).attr("href");
    $(".collapse").not(target).collapse("hide");
    $(".nav-item").not($(this).parent()).removeClass("active");
  });
});


