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



//  handle the toggle of the d=side nav 

// document.addEventListener("DOMContentLoaded", function () {
//   const body = document.body;
//   const toggler = document.querySelector("#customSidebarToggle");

//   toggler.addEventListener("click", function () {
//     if (body.classList.contains("g-sidenav-pinned")) {
//       // currently open → close
//       body.classList.remove("g-sidenav-pinned");
//       body.classList.add("g-sidenav-hidden");
//     } else {
//       // currently closed → open
//       body.classList.remove("g-sidenav-hidden");
//       body.classList.add("g-sidenav-pinned");
//     }
//   });
// });

$(document).ready(function () {
  const toggler = $(".sidenav-toggler");

  toggler.on("click", function () {
    if (window.innerWidth >= 1200) {
      // Desktop → pinned toggle
      $("body").removeClass().addClass("g-sidenav-pinned");
      // If already pinned, unpin
      if ($("body").hasClass("g-sidenav-pinned")) {
        $("body").removeClass("g-sidenav-pinned");
      } else {
        $("body").addClass("g-sidenav-pinned");
      }
    } else {
      // Mobile → overlay toggle
      if ($("body").hasClass("g-sidenav-show")) {
        $("body").removeClass("g-sidenav-show nav-open");
        $(".sidenav-backdrop").remove();
      } else {
        $("body").removeClass().addClass("g-sidenav-show nav-open");
        $("body").append('<div class="sidenav-backdrop"></div>');
      }
    }
  });

  // Backdrop click always closes
  $(document).on("click", ".sidenav-backdrop", function () {
    $("body").removeClass("g-sidenav-show nav-open");
    $(".sidenav-backdrop").remove();
  });
});

//  



