// console.log("custom.js loaded");

// let formInitialized = false;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    for (let cookie of document.cookie.split(";")) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// $(document).ready(function () {
//  $.ajax({
//   url: '/api/rental-deals/filter',
//   method: 'POST',
//   headers: {
//     'X-CSRFToken': getCookie('csrftoken')
//   },
//   contentType: 'application/json',
//   data: JSON.stringify({ draw: 1, start: 0, length: 10, type: "All" }),  // example data
//   success: function (data) {
//     console.log("✅ Success:", data);
//   },
//   error: function (xhr, status, error) {
//     console.error("❌ Error:", status, error);
//     console.error("Response Text:", xhr.responseText);
//   },
//   complete: function (xhr) {
//     console.log("📦 Raw Response:", xhr);
//   }
// });
// });

function getTypeFromURL() {
  const lastPart = window.location.pathname
    .split("/")
    .filter(Boolean)
    .slice(-1)[0];

  const mapping = {
    list: "All",
    draft: "draft",
    approved: "approved",
    pending: "pending",
    waiting: "waiting",
    rejected: "rejected",
    "entered-finance": "entered-finance",
    "pending-finance": "pending-finance",
  };

  return mapping[lastPart] || null;
}

$(document).ready(function () {
  const type = getTypeFromURL();
  let headingText =
    (type ? type[0].toUpperCase() + type.slice(1) : "") + " Rental Deals";
  $("#heading").text(headingText);
});

$(document).ready(function () {
  console.log(getTypeFromURL());
  const table = $("#myTable").DataTable({
    scrollY: "600px", // Set the height you want
    scrollCollapse: true,
    paging: true,
    processing: true,
    serverSide: true,
    ajax: {
      url: "/api/rental-deals/filter",
      type: "POST",
      processData: false,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      contentType: "application/json",
      data: function (d) {
        d.draw = d.draw;
        d.start = d.start;
        d.length = d.length;
        d.type = getTypeFromURL();
        const formData = $("#filterForm").serializeArray();
        formData.forEach((field) => {
          if (field.name === "from_date" || field.name === "to_date") {
            // Format manually to YYYY-MM-DD if value is present
            if (field.value) {
              const date = new Date(field.value);
              const formatted = date.toISOString().split("T")[0]; // YYYY-MM-DD
              d[field.name] = formatted;
            }
          } else {
            d[field.name] = field.value;
          }
        });

        console.log("➡️ Sending Data:", JSON.stringify(d, null, 2));
        return JSON.stringify(d);
      },
      dataSrc: function (json) {
        console.log("Full JSON response:", json); // 🔍 all data
        console.log("Only table rows:", json.data); // 🔍 just the rows
        return json.data; // required — tells DataTables where the table rows are
      },

      // complete: function (xhr, status) {
      //   // Log the full response object
      //   console.log("Raw response:", xhr);
      //   // Log the parsed JSON response (if available)
      //   try {
      //     console.log("Parsed response:", JSON.parse(xhr.responseText));
      //   } catch (e) {
      //     console.log("Response is not valid JSON");
      //   }
      // },
    },
    success: function (data) {
      console.log("✅ Success:", data);
    },
    columns: [
      {
        data: null,
        title: "Actions",
        render: function (data, type, row, meta) {
          return `
                <a href="/rental-deals/${row.id}/" class="text-primary"><i class="fas fa-eye"></i></a>
                <a href="/rental-deals/${row.id}/update/" class="text-warning mx-2"><i class="fas fa-edit"></i></a>
                <a href="/rental-deals/${row.id}/delete/" class="text-danger"><i class="fas fa-trash"></i></a>
              `;
        },
      },
      { data: "email", title: "submitted_by_user" },
      { data: "reference_number", title: "Reference Number" },
      {
        data: "date",
        title: "Deal Date",
        render: function (data) {
          return new Date(data).toLocaleDateString(); // ✅ format: M/D/YYYYsss
        },
      },

      { data: "unit_details", title: "Unit No" },
      { data: "building_name", title: "Building Name" },

      { data: "project_name", title: "Project Name" },
      { data: "rental_price", title: "Rental Price" },

      {
        data: "deal_end_date",
        title: "End Date",
        render: function (data) {
          return new Date(data).toLocaleDateString();
        },
      },
      {
        data: "deal_start_date",
        title: "Start Date",
        render: function (data) {
          return new Date(data).toLocaleDateString();
        },
      },
      {
        data: "submitted_date",
        title: "Submitted Date",
        render: function (data) {
          return new Date(data).toLocaleDateString(); // ✅ format: M/D/YYYY
        },
      },
    ],
  });

  // Reload table when filters change
  // $("#typeFilter, #fromDate, #toDate, #refNumber").on(
  //   "change keyup",
  //   function () {
  //     table.ajax.reload();
  //   }
  // );
  $("#filterForm").on("submit", function (e) {
    e.preventDefault(); // Prevent page reload
    table.ajax.reload(); // Reload DataTable with new filters
  });
});

// dropdown for side nav

$(document).ready(function () {
  // Get current URL path
  const path = window.location.pathname;

  // Check if current URL is under /rental-deals/
  if (path.startsWith("/rental-deals/")) {
    // Expand the submenu
    $("#rentalDealsSubmenu").addClass("show");

    // Highlight the parent nav link (optional for styling)
    $("[href='#rentalDealsSubmenu']").removeClass("collapsed");

    // Highlight the correct submenu item
    $("#rentalDealsSubmenu a").each(function () {
      if ($(this).attr("href") === path) {
        $(this).parent("li").addClass("active");
      }
    });
  }
});

// breadcumd heading showing all deals
