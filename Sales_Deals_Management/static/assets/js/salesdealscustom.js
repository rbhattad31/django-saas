console.log("custom.js loaded");

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
//   if (!formInitialized) {
//     console.log("Form not initialized, setting up.");
//     // Initialize form elements here

//     console.log("Document is ready!");

//     // Handle form submission
//     $("#filterForm").on("submit", function (e) {
//       e.preventDefault();

//       const formData2 = Object.fromEntries(
//         new URLSearchParams($(this).serialize())
//       ); // serialize form fields
//       console.log("Form data:", formData2); // Log the serialized form data
//       postAndRedirect("/sales-deals/filter/", formData2);
//     });
//     $("#filterForm").trigger("submit");
//     formInitialized = true; // Set the flag to true after initialization
//   }
// });

// function postAndRedirect(postUrl, formData1) {
//   const formData = new FormData();

//   const lastPart = window.location.pathname
//     .split("/")
//     .filter(Boolean)
//     .slice(-1)[0];
//   console.log(lastPart);

//   for (const key in formData1) {
   
//     if (lastPart === "all" && key === "type") {
      
//       formData.append(key, "All");
//       console.log(`Appending ${key}: all`,  );;
//     }
//     else if (lastPart === "draft" && key === "type") {
//       formData.append(key, "draft");
//       console.log(`Appending ${key}: draft`,  );;
//     }  
//     else if (lastPart === "approved" && key === "type") {
//       formData.append(key, "approved");
//       console.log(`Appending ${key}: approved`,  );;
//     }  
//     else if (lastPart === "pending" && key === "type") {
//       formData.append(key, "pending");
//       console.log(`Appending ${key}: pending`,  );;
//     }  
//     else if (lastPart === "waiting" && key === "type") {
//       formData.append(key, "waiting");
//       console.log(`Appending ${key}: waiting`,  );;
//     }  
//     else if (lastPart === "rejected" && key === "type") {
//       formData.append(key, "rejected");
//       console.log(`Appending ${key}: rejected`,  );;
//     }  
//     else if (lastPart === "entered-finance" && key === "type") {
//       formData.append(key, "entered-finance");
//       console.log(`Appending ${key}: entered-finance`,  );;
//     }  

//     else if (lastPart === "waiting-finance" && key === "type") {
//       formData.append(key, "waiting-finance");
//       console.log(`Appending ${key}: waiting-finance`,  );;
//     }  
    

//     else {
//       formData.append(key, formData1[key]);
//     }

     
//   }

//   console.log("Form data to be sent:", formData);

//   fetch(postUrl, {
//     method: "POST",
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     body: formData,
//     credentials: "include",
//   })
//     .then((response) => {
//       console.log("Response status:", response.status);
//       return response.json();
//     })
//     .then((data) => {
//       console.log("Response data:", data.data);
//       const rentalDeals = data.data || data; // use data.data if your API wraps it

//       $("#myTable").DataTable({
//         data: rentalDeals, // ✅ Pass the array directly
//         destroy: true, // ❗Needed if reinitializing table
//         columns: [
//           {
//             data: null,
//             title: "Action",
//             render: function (data, type, row) {
//               return `
//                 <a href="/sales-deals/view/${row.id}/" class="text-primary"><i class="fas fa-eye"></i></a>
//                 <a href="/sales-deals/update/${row.id}/" class="text-warning mx-2"><i class="fas fa-edit"></i></a>
//                 <a href="/sales-deals/delete/${row.id}/" class="text-danger"><i class="fas fa-trash"></i></a>
//               `;
//             },
//             orderable: false,
//             searchable: false
//           },
//           { data:"submitted_by_user", title: "Submitted By User"},
//           { data: "reference_number", title: "Reference Number" },
//           {
//             data:"deal_date",title: "Deal Date",
//             render: function (data) {
//               return new Date(data).toLocaleDateString(); // Format date      
//             } 
//           },  
//           {data:"unit_details", title: "Unit No"},  


//           { data: "builduing_name", title: "Building Name" }, 
//           { data: "project_name", title: "Project Name" },  
//           {data:"deal_amount", title: "Selling Price"},   
//           { 
//             data: "submitted_date",   
//             title: "Submitted Date",  
//             render: function (data) {     
//               return new Date(data).toLocaleDateString(); // Format date
//             },
//           },
//         ],
//       });
//     })
//     .catch((error) => {
//       console.error("POST error:", error);
//     });
// }
// document.addEventListener("DOMContentLoaded", function () {
//   const dropdownIds = ['rentalDealsSubmenu', 'salesDealsSubmenu'];

//   dropdownIds.forEach(id => {
//     const collapseEl = document.getElementById(id);
//     const state = localStorage.getItem(id + '_open');

//     if (state === 'true') {
//       new bootstrap.Collapse(collapseEl, { toggle: true });
//     }

//     collapseEl.addEventListener('show.bs.collapse', () => {
//       localStorage.setItem(id + '_open', 'true');
//     });
//     collapseEl.addEventListener('hide.bs.collapse', () => {
//       localStorage.setItem(id + '_open', 'false');
//     });
//   });
// });

// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== "") {
//     for (let cookie of document.cookie.split(";")) {
//       cookie = cookie.trim();
//       if (cookie.startsWith(name + "=")) {
//         cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }

// // $(document).ready(function () {
// //  $.ajax({
// //   url: '/api/rental-deals/filter',
// //   method: 'POST',
// //   headers: {
// //     'X-CSRFToken': getCookie('csrftoken')
// //   },
// //   contentType: 'application/json',
// //   data: JSON.stringify({ draw: 1, start: 0, length: 10, type: "All" }),  // example data
// //   success: function (data) {
// //     console.log("✅ Success:", data);
// //   },
// //   error: function (xhr, status, error) {
// //     console.error("❌ Error:", status, error);
// //     console.error("Response Text:", xhr.responseText);
// //   },
// //   complete: function (xhr) {
// //     console.log("📦 Raw Response:", xhr);
// //   }
// // });
// // });


// gopi code

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
    "pending-finance": "pending-finance",
    "entered-finance": "entered-finance",
  };
    

  return mapping[lastPart] || null;
}


$(document).ready(function () {
 
  const type = getTypeFromURL();
  let headingText = (type ? type[0].toUpperCase() + type.slice(1) : '') + ' Sales Deals';
  $('#saleheading').text(headingText);

   
});
 

  

 
 
$(document).ready(function () {
 
  
  console.log(getTypeFromURL());
  const table = $("#myTable").DataTable({
    scrollY: '400px',
    scrollX: true,
    scrollCollapse: true,
    fixedColumns: true,
    paging: true,
    processing: true,
    searching: true,
    order: [[7, "desc"]], // Default order by "Submitted Date" descending
    serverSide: true,
    ajax: {
      url: "/sales-deals/filter/",
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
        d.type =  getTypeFromURL();
          const formData = $('#filterForm').serializeArray();
          formData.forEach(field => {
           if (field.name === 'from_date' || field.name === 'to_date') {
      // Format manually to YYYY-MM-DD if value is present
      if (field.value) {
        const date = new Date(field.value);
        const formatted = date.toISOString().split('T')[0]; // YYYY-MM-DD
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
              <a href="/sales-deals/view/${row.id}/" class="text-primary"><i class="fas fa-eye"></i></a> 
              <a href="/sales-deals/update/${row.id}/" class="text-warning mx-2"><i class="fas fa-edit"></i></a>
              <a href="#" class="text-danger delete-link" data-id="${row.id}"><i class="fas fa-trash"></i></a>
            `;
        },
      },
      { data:"email", title: "Submitted By User"},
      { data: "reference_number", title: "Reference Number" },
      {
        data:"date",title: "Deal Date",
        render: function (data) {
          return new Date(data).toLocaleDateString(); // Format date      
        }
      },  
      {data:"unit_details", title: "Unit No"},  


      { data: "builduing_name", title: "Building Name" }, 
      { data: "project_name", title: "Project Name" },  
      {data:"deal_amount", title: "Selling Price"},   
      { 
        data: "submitted_date",   
        title: "Submitted Date",  
            render: function (data) {     
              return new Date(data).toLocaleDateString(); // Format date
            },
          },
        ],
      });
    })

// When user clicks the trash icon — open modal
    $(document).on("click", ".delete-btn", function (e) {
      e.preventDefault();
      selectedDealId = $(this).data("id");
      $("#deleteModal").modal("show");
    });
    
    // When user confirms delete in modal
    $("#confirmDeleteBtn").on("click", function () {
      if (!selectedDealId) return;
    
      $.ajax({
        url: `/sales-deals/${selectedDealId}/delete/`, // NOT /delete/
        type: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
          console.log("Deleted!");
            $("#deleteModal").modal("hide");
 
      // Refresh DataTable or reload page
            $("#myTable").DataTable().ajax.reload(null, false);
        },
        error: function (e) {
        console.log(e);
        alert("Error deleting record");
      },
      });

    });
    // .catch((error) => {
    //   console.error("POST error:", error);
    // });

//   // Reload table when filters change
//   // $("#typeFilter, #fromDate, #toDate, #refNumber").on(
//   //   "change keyup",
//   //   function () {
//   //     table.ajax.reload();
//   //   }
//   // );
//    $('#filterForm').on('submit', function (e) {
//     e.preventDefault(); // Prevent page reload
//     table.ajax.reload(); // Reload DataTable with new filters
//   });
// });

// // dropdown for side nav
// document.addEventListener("DOMContentLoaded", function () {
//   const dropdownIds = ['rentalDealsSubmenu', 'salesDealsSubmenu'];

//   dropdownIds.forEach(id => {
//     const collapseEl = document.getElementById(id);
//     const state = localStorage.getItem(id + '_open');

//     if (state === 'true') {
//       new bootstrap.Collapse(collapseEl, { toggle: true });
//     }

//     collapseEl.addEventListener('show.bs.collapse', () => {
//       localStorage.setItem(id + '_open', 'true');
//     });
//     collapseEl.addEventListener('hide.bs.collapse', () => {
//       localStorage.setItem(id + '_open', 'false');
//     });
//   });
// });

   $(document).ready(function () {
    // Get current URL path
    const path = window.location.pathname;
    

    // Check if current URL is under /rental-deals/
    if (path.startsWith("/sales-deals/")) {
      // Expand the submenu
      $("#salesDealsSubmenu").addClass("show");

      // Highlight the parent nav link (optional for styling)
      $("[href='#salesDealsSubmenu']").removeClass("collapsed");

      // Highlight the correct submenu item
      $("#salesDealsSubmenu a").each(function () {
        if ($(this).attr("href") === path) {
          $(this).parent("li").addClass("actived");
        }
      });
    }
  });


let selectedDealId = null;
 
// When user clicks the trash icon — open modal
$(document).on("click", ".delete-link", function (e) {
  e.preventDefault();
  selectedDealId = $(this).data("id");
  $("#deleteModal").modal("show");
});


$(document).ready(function () {
  // Go forward to next tab
  $("#changeTabToSource").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-source-tab")
    ).show();
  });
 
  $("#changeTabToAgency").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-agency-tab")
    ).show();
  });
 
  $("#changeTabToRevenue").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-revenue-tab")
    ).show();
  });
 
  $("#changeTabToDocuments").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-documents-tab")
    ).show();
  });
 
  $("#changeTabToComments").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-comments-tab")
    ).show();
  });
 
  // Go back to previous tab
  $("#previousTab1").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-property-tab")
    ).show();
  });
 
  $("#previousTab2").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-source-tab")
    ).show();
  });
 
  $("#previousTab3").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-agency-tab")
    ).show();
  });
 
  $("#previousTab4").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-revenue-tab")
    ).show();
  });
 
  $("#previousTab5").on("click", function () {
    bootstrap.Tab.getOrCreateInstance(
      document.querySelector("#nav-documents-tab")
    ).show();
  });
});