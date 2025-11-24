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
    waiting: "waiting",//This is related to Waiting Finance.
    rejected: "rejected",
    "entered-finance": "entered-finance",
    "waiting-finance": "waiting-finance",//This is related to pending finance
  };
    
  
  // const result = mapping[lastPart] || null;
  //  // Debug line

  // return result;
  return mapping[lastPart] || null;
}



// $(document).ready(function () {
 
//   const type = getTypeFromURL();
//   let headingText = (type ? type[0].toUpperCase() + type.slice(1) : '') + 'Properties';
//   $('#propertyheading').text(headingText);

   
// });
$(document).ready(function () {
  let headingText = 'Properties';
  console.log("Heading text set to:", headingText);

  $('#propertyheading').text(headingText);
});


$(document).ready(function () {
  
  console.log(getTypeFromURL());
  const table = $("#myTable").DataTable({
    pagingType: "simple_numbers",
    renderer: "bootstrap",
    scrollY: "600px", // Set the height you want
    scrollCollapse: true,
    // dom: '<"d-flex justify-content-between align-items-center mb-3"Bf>rtip',
    dom: '<"d-flex justify-content-between align-items-center mb-3"<"dt-buttons-left"B><"dt-filter-right"f>>rti<"d-flex justify-content-end"p><"clear">',

    // dom: 
    // "<'row mb-3'<'col-md-6'B><'col-md-6'f>>" + 
    // "<'row'<'col-12'tr>>" + 
    // "<'row mt-3'<'col-md-6'i><'col-md-6'p>>",
    // pagingType: 'full_numbers',
    buttons: [
      'excelHtml5',
      'pdfHtml5'
    ],
    
    processing: true,
    serverSide: true,
    ordering: true,
    order: [[1, 'desc']], // Default sort on the second column (optional)
    // dom: 'Bfrtip', // Add buttons to the table
    
    buttons: [
        
        {
            extend: 'excelHtml5',
            text: '<i class=""></i> Excel',
            titleAttr: 'Export to Excel',
            className: 'btn btn-success btn-sm', // Custom styling
            // exportOptions: {
            //     columns: ':visible' // Export only visible columns
            // }
        },
        {
            extend: 'pdfHtml5',
            text: '<i class=""></i> PDF',
            titleAttr: 'Export to PDF',
            className: 'btn btn-danger btn-sm',
            orientation: 'landscape',
            pageSize: 'A4',
            // exportOptions: {
            //     columns: ':visible'
            // }
        }
    ],
    drawCallback: function () {
          // Optional: add any custom JS you want on draw
          // Example: add class if needed (but your CSS should handle it)
          $('.dataTables_paginate .page-link').addClass('page-link');
    },
   
    ajax: {
      // url: "/api/rental-deals/filter",
      url: "/rental-properties/filter/",
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
        d.order = d.order; // Add this to send ordering information
        d.type =  getTypeFromURL();
        console.log("🔍 Order data before sending:", JSON.stringify(d.order, null, 2)); // Debug order
        console.log("🔍 d.type:", d.type);
        const formData = $('#filterForm').serializeArray();
        // formData.forEach(field => {
            
        //    if (field.name === 'tenancy_start_date' ||field.name === 'tenancy_end_date' ||field.name === 'deal_date' ||field.name === 'deal_date_to' ||field.name === 'pm_start_date' ||field.name === 'pm_end_date') {
        //         if (field.value) {
        //             // Format date as DD-MM-YYYY (if your backend expects that)
        //             const dateObj = new Date(field.value);
        //             const day = ("0" + dateObj.getDate()).slice(-2);
        //             const month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
        //             const year = dateObj.getFullYear();
        //             d[field.name] = `${day}-${month}-${year}`;
        //         }
               
        //         return;  
        //     }
        //    if (field.name === 'type'){
        //       console.log("TYPE IN SIDE POINT x1") 
        //       return;
        //    }            
        //    if (field.name === 'from_date' || field.name === 'to_date'|| field.name === 'tenancy_start_date') {
        //     if(field.name === 'tenancy_start_date'){
        //         console.log("Raw tenancy_start_date value:", field.value);
        //     }
        //     // Format manually to YYYY-MM-DD if value is present
        //     if (field.value) {
        //       const date = new Date(field.value);
        //       const formatted = date.toISOString().split('T')[0]; // YYYY-MM-DD
        //       d[field.name] = formatted;
        //     }
        //   } else {
        //     d[field.name] = field.value;
        //   }
        // });
        
        formData.forEach(field => {
            if (field.name === 'tenancy_start_date' || field.name === 'tenancy_end_date' || field.name === 'deal_date' || field.name === 'submitted_date' || field.name === 'pm_start_date' || field.name === 'pm_end_date') {
                if (field.value) {
                    // Format date as DD-MM-YYYY
                    const dateObj = new Date(field.value);
                    const day = ("0" + dateObj.getDate()).slice(-2);
                    const month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
                    const year = dateObj.getFullYear();
                    d[field.name] = `${day}-${month}-${year}`;
                } else {
                    d[field.name] = null;  // Explicitly send null for empty dates
                }
                return;
            }
            if (field.name === 'type'){
                console.log("TYPE IN SIDE POINT x1")
                return;
            }
            if (field.name === 'from_date' || field.name === 'to_date' || field.name === 'tenancy_start_date') {
                if(field.name === 'tenancy_start_date'){
                    console.log("Raw tenancy_start_date value:", field.value);
                }
                // Format manually to YYYY-MM-DD if value is present
                if (field.value) {
                    const date = new Date(field.value);
                    const formatted = date.toISOString().split('T')[0]; // YYYY-MM-DD
                    d[field.name] = formatted;
                } else {
                    d[field.name] = null;  // Add this for consistency with other dates
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
      error: function (xhr, status, error) {
        console.error("❌ AJAX Error:", status, error, xhr.responseText); // Log AJAX errors
      },
      
    },
      success: function (data) {
        console.log("✅ Success:", data);
      },
    columns: [
      {
        data: null,
        title: "Actions",
        orderable: false,
        render: function (data, type, row, meta) {
          console.log("Full row object:", row);
          console.log("Row status:", row.status);
          console.log(data);
          //           return `
          //                 <a href="/rental-deals/view/${row.id}/" class="text-primary"><i class="fas fa-eye"></i></a>
          //                 <a href="/rental-deals/update/${row.id}/" class="text-warning mx-2" id="editDealBtn" data-deal-id="${row.id}"><i class="fas fa-edit"></i></a>
 
          //                 <a href="#" class="text-danger delete-btn" data-id="${row.id}" data-bs-toggle="modal" data-bs-target="#deleteModal">
          //   <i class="fas fa-trash"></i>
          // </a>
          //               `;
          let actionsHtml =""
          if(row.can_view){
            console.log("in hte can _view")
          actionsHtml += `
                                <a href="/rental-properties/${row.id}/view/" class="text-primary"><i class="fas fa-eye"></i></a>
                            `;
          }
          // Conditionally add the Edit button
          if (row.can_edit ) {
            if(row.is_approved_rejected=='A' && !(row.can_edit_approved)){
              actionsHtml += ""
                               
            }
            else{
              actionsHtml += `
                                     <a href="/rental-properties/${row.id}/edit/" class="text-warning mx-2"><i class="fas fa-edit"></i></a>
                                `;
            }
            
            
          } 
         
 
          // Conditionally add the Delete button
          if (row.can_delete) {
            actionsHtml += `
                                   <a href="#" class="text-danger delete-link" data-id="${row.id}"><i class="fas fa-trash"></i></a>
                                `;
          } 

          if(row.status=='Expired'||row.status=='About To Expire'){
                actionsHtml += `
                  <a href="/rental-properties/${row.id}/renew/" class="text-primary mr-2" title="Renew Property">
                    <i class="fas fa-spinner"></i>
                  </a>
                `;
          }

           
          return actionsHtml;
        }
      },
      { data: "id", title: "Property Id" },
      { data: "reference_number", title: "Reference Number", className: "editable" },
      { data: "deal_date", title: "Deal Date" },
      { data: "unit_details", title: "Unit No", className: "editable" },
      { data: "building_name", title: "Building Name", className: "editable" },
      { data: "project_name", title: "Project Name", className: "editable" },
      { data: "pms_price", title: "PMS Price", className: "editable" },
      { data: "pm_start_date", title: "PM Start Date" },
      { data: "pm_end_date", title: "PM End Date" },
      { data: "tenancy_start_date", title: "Tenancy Start Date" },
      { data: "tenancy_end_date", title: "Tenancy End Date" },
      // { data: "submitted_date", title: "Submitted Date"},
      {
        data: "submitted_date",
        title: "Submitted Date",
        render: data => new Date(data).toLocaleDateString()
      },
      { data: "status", title: "Status" },

      // addtional fields which adre invisible for the  Excel data export
      { data: "owner_first_name", title: "Owner First Name", visible: false },
      { data: "owner_source", title: "Owner Source", visible: false },
      { data: "owner_mobile", title: "Owner Mobile", visible: false },
      { data: "owner_email", title: "Owner Email", visible: false },
      { data: "agency_name", title: "Agency Name", visible: false },
      { data: "agent_name", title: "Agent Name", visible: false },
      { data: "brn", title: "BRN", visible: false },
      { data: "agent_phone", title: "Agent Phone", visible: false },
      { data: "agent_email", title: "Agent Email", visible: false },
      { data: "no_of_cheque", title: "No of Cheque", visible: false },
      { data: "cheque_date", title: "Cheque Date", visible: false },
      
      { data: "kyc_number", title: "KYC Number", visible: false },
      { data: "total_commission", title: "Total Commission", visible: false },
      { data: "less_outside_commission", title: "Less Outside Commission", visible: false },
      { data: "net_commission", title: "Net Commission", visible: false },
      { data: "classic", title: "Classic", visible: false },
      { data: "agent1", title: "Agent 1", visible: false },
      { data: "agent2", title: "Agent 2", visible: false },
      { data: "agent3", title: "Agent 3", visible: false },
      { data: "comments", title: "Comments", visible: false },
      { data: "agent_name1_display", title: "Agent Name 1", visible: false },
      { data: "agent_name2_display", title: "Agent Name 2", visible: false },
      { data: "agent_name3_display", title: "Agent Name 3", visible: false },
      { data: "receipt_no", title: "Receipt No", visible: false },
      { data: "form_status", title: "Form Status", visible: false },
      { data: "created_at", title: "Created At", visible: false },
      { data: "updated_at", title: "Updated At", visible: false },
      { data: "created_by", title: "Created By", visible: false },
      { data: "updated_by", title: "Updated By", visible: false },
      { data: "status", title: "Status", visible: false },
      { data: "deal_sno", title: "Deal SNO", visible: false },
      { data: "is_approved_rejected_display", title: "Approved/Rejected", visible: false },
      { data: "approved_rejected_by", title: "Approved Rejected By", visible: false },
      { data: "is_entered_in_finance_system_display", title: "Entered Finance System", visible: false },
      { data: "comments_finance", title: "Finance Comments", visible: false },
      { data: "submitted_by_user_id", title: "Submitted By User ID", visible: false },
      { data: "is_deleted", title: "Is Deleted", visible: false },
      { data: "agent_comment", title: "Agent Comment", visible: false },
      { data: "is_property_aml", title: "Property AML", visible: false },
      { data: "screening", title: "Screening", visible: false },
      { data: "screening_comments", title: "Screening Comments", visible: false },
      { data: "seller_nationality", title: "Seller Nationality", visible: false },
      { data: "buyer_nationality", title: "Buyer Nationality", visible: false },
      // { data: "manager_approved_rejected", title: "Manager Approval", visible: false },

      
    ],
  });


  // Change table length
  $('select[name="length"]').on('change', function () {
    table.page.len(parseInt($(this).val()) || 10).draw();
  });

  let selectedDealId = null;

  // When trash icon or delete link is clicked
  $(document).on("click", ".delete-link", function (e) {
    e.preventDefault();
    selectedDealId = $(this).data("id");
    $("#deleteModal").modal("show");
  });

  // When user confirms deletion in modal
  // $("#confirmDeleteBtn").on("click", function () {
  //   if (!selectedDealId) return;

  //   $.ajax({
  //     url: `/rental-properties/${selectedDealId}/delete/`,
  //     //type: "POST", // or "DELETE" if your backend expects that
  //     type: "DELETE",
  //     headers: {
  //       "X-CSRFToken": getCookie("csrftoken"),
  //     },
  //     success: function () {
  //       $("#deleteModal").modal("hide");
  //       alert("Property deleted successfully.");
  //       $("#myTable").DataTable().ajax.reload(null, false); // Refresh DataTable
  //     },
  //     error: function (xhr) {
  //       alert("Error deleting property: " + (xhr.responseJSON?.message || "Unknown error"));
  //     },
  //   });
  // });
  // Confirm delete in modal
  $("#confirmDeleteBtn").on("click", function () {
      if (!selectedDealId) return;

      $.ajax({
        url: `/rental-properties/${selectedDealId}/delete/`,
        type: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
          $("#deleteModal").modal("hide");
          alert("Property deleted successfully.");

          // Remove the row immediately from DataTable
          const row = $(`#myTable .delete-link[data-id='${selectedDealId}']`).closest('tr');
          table.row(row).remove().draw(false);

          // Or reload the table (if you prefer this instead of manual row remove)
          // table.ajax.reload(null, false);
        },
        error: function (xhr) {
          alert("Error deleting property: " + (xhr.responseJSON?.message || "Unknown error"));
        },
      });
    });

 
   $('#filterForm').on('submit', function (e) {
    e.preventDefault(); // Prevent page reload
    table.ajax.reload(); // Reload DataTable with new filters
  });
  
});


// $(document).ready(function () {
//   // Get current URL path
//   const path = window.location.pathname;
//   console.log("Current path:", path);

//   // Check if current URL is under /rental-deals/
//   if (path.startsWith("/rental-properties/")) {
//     // Expand the submenu
//     $("#rentalPropertySubmenu").addClass("show");

//     // Highlight the parent nav link (optional for styling)
//     $("[href='#rentalPropertySubmenu']").removeClass("collapsed");

//     // Highlight the correct submenu item
//     $("#rentalPropertySubmenu a").each(function () {
//       if ($(this).attr("href") === path) {
//        $(this).parent("li").addClass("active");

//       }
//     });
//   }
// });
console.log("Entering into path")
// $(document).ready(function () {
//   const path = window.location.pathname.replace(/\/$/, "");
//   console.log("Current path:", path);

//   if (path.startsWith("/rental-properties")) {
//     $("#rentalPropertySubmenu").addClass("show");
//     $("[href='#rentalPropertySubmenu']").removeClass("collapsed");

//     $("#rentalPropertySubmenu a").each(function () {
//       const linkHref = $(this).attr("href").replace(/\/$/, "");
//       if (linkHref === path) {
//         $(this).parent("li").addClass("active");
//       }
//     });
//   }
// });
// $(document).ready(function () {
//   const path = window.location.pathname.replace(/\/$/, ""); // remove trailing slash
//   console.log("🔍 Current path:", path);

//   if (path.startsWith("/rental-properties")) {
//     $("#rentalPropertySubmenu").addClass("show");
//     $("[href='#rentalPropertySubmenu']").removeClass("collapsed");

//     $("#rentalPropertySubmenu a").each(function () {
//       const linkHref = $(this).attr("href").replace(/\/$/, "");
//       if (linkHref === path) {
//         // ✅ Highlight <a> directly
//         $(this).addClass("active");

//         // ✅ Also highlight parent <li> if it exists
//         $(this).parent("li").addClass("active");
//       }
//     });
//   }
// });
$(document).ready(function () {
  const path = window.location.pathname.replace(/\/$/, ""); // remove trailing slash
  console.log("🔍 Current path:", path);

  if (path.startsWith("/rental-properties")) {
    console.log("🏠 Property Management path matched.");
    
    // Expand the submenu
    $("#propertySubmenu").addClass("show");
    $("[href='#propertySubmenu']").removeClass("collapsed").attr("aria-expanded", "true");
    console.log("📂 Submenu #propertySubmenu opened.");

    // Loop through links inside submenu
    $("#propertySubmenu a").each(function () {
      const linkHref = $(this).attr("href").replace(/\/$/, "");
      console.log("🔗 Found submenu link:", linkHref);

      if (linkHref === path) {
        console.log("✅ Match found for:", linkHref);

        // Highlight the link and parent <li>
        $(this).addClass("active-item");
        $(this).parent("li").addClass("active-item");
      } else {
        console.log("❌ No match for:", linkHref);
      }
    });

  }
});




//Delete Script

let selectedDealId = null;
 
// When user clicks the trash icon — open modal
$(document).on("click", ".delete-btn", function () {
  selectedDealId = $(this).data("id");
  $("#deleteModal").modal("show");
});
 
// When user confirms delete in modal



function loadAgentDropdown(requestdata) {
  $.ajax({
    url: "/api/agents/dropdown/",
    type: "GET",
    success: function (agents) {
      populateAgentDropdown(
        "#submitted_by_agent",
        agents,
        requestdata.submitted_by_agent
      );
      populateAgentDropdown("#agent_name1", agents, requestdata.agent_name1);
      populateAgentDropdown("#agent_name2", agents, requestdata.agent_name2);
      populateAgentDropdown("#agent_name3", agents, requestdata.agent_name3);
    },
    error: function () {
      console.error("Failed to load agents.");
    },
  });
}

// populate the user data based on requriement

function populateAgentDropdown(selector, data, selectedId = null) {
  const $dropdown = $(selector);
  $dropdown.empty().append('<option value="">Select Agent</option>');

  data.forEach(function (agent) {
    const isSelected = selectedId == agent.id ? "selected" : "";
    $dropdown.append(
      `<option value="${agent.id}" ${isSelected}>${agent.name}</option>`
    );
  });
}

