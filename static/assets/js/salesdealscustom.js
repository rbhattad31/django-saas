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
function parseReceiptsList(receiptsListValue) {
  if (!receiptsListValue) {
    return [];
  }

  if (Array.isArray(receiptsListValue)) {
    return receiptsListValue;
  }

  try {
    const parsedValue = JSON.parse(receiptsListValue);
    return Array.isArray(parsedValue) ? parsedValue : [];
  } catch (error) {
    console.warn("Unable to parse receipts_list", error);
    return [];
  }
}

function getReceiptSelects() {
  return $("select[name^='receipt_no'], select[name^='receipt_extra_']");
}

function getDynamicReceiptSelects() {
  return $("select[name^='receipt_extra_']");
}

function getReceiptNumberFromId(receiptId) {
  const receipt = (sales_data.receipts || []).find(function (item) {
    return String(item.id) === String(receiptId);
  });

  return receipt ? receipt.receipt_number : "";
}

function collectSelectedReceipts() {
  const selectedReceipts = [];
  const seenIds = new Set();

  getDynamicReceiptSelects().each(function () {
    const value = String($(this).val() || "").trim();

    if (!value || !/^\d+$/.test(value) || seenIds.has(value)) {
      return;
    }

    const receiptNumber = getReceiptNumberFromId(value);
    if (!receiptNumber) {
      return;
    }

    selectedReceipts.push({
      id: parseInt(value, 10),
      receipt_number: receiptNumber,
    });
    seenIds.add(value);
  });

  return selectedReceipts;
}

function syncReceiptsListField() {
  const selectedReceipts = collectSelectedReceipts();
  $("#receipts_list").val(JSON.stringify(selectedReceipts));
  return selectedReceipts;
}

function syncReceiptsList() {
  return syncReceiptsListField();
}

function refreshReceiptOptionStates() {
  const receiptSelects = getReceiptSelects();
  const selectedIds = receiptSelects
    .map(function () {
      return String($(this).val() || "").trim();
    })
    .get()
    .filter(function (value) {
      return /^\d+$/.test(value);
    });

  receiptSelects.each(function () {
    const currentValue = String($(this).val() || "").trim();

    $(this)
      .find("option")
      .each(function () {
        const optionValue = String($(this).val() || "").trim();

        if (!/^\d+$/.test(optionValue)) {
          $(this).prop("disabled", false);
          return;
        }

        const shouldDisable =
          selectedIds.includes(optionValue) && optionValue !== currentValue;
        $(this).prop("disabled", shouldDisable);
      });
  });

  refreshAddReceiptButtonState();
  syncReceiptsListField();
}

function refreshAddReceiptButtonState() {
  const receiptSelects = getReceiptSelects();
  const allFilled =
    receiptSelects.length > 0 &&
    receiptSelects.toArray().every(function (field) {
      const value = String($(field).val() || "").trim();
      if (!value) return false;
      if (value === "Null") return false;
      if (value === "No Commission" || value === "No Commision") return false;
      return /^\d+$/.test(value);
    });

  $("#addReceiptBtn").prop("disabled", !allFilled);
}

function addReceiptRow(selectedValue = "", selectedReceiptNumber = "") {
  const nextIndex = $(".dynamic-receipt-row").length + 1;
  const rowId = `receipt_extra_${nextIndex}`;
  const rowMarkup = `
    <div class="col-md-6 mb-2 dynamic-receipt-row" data-row-index="${nextIndex}">
      <div class="d-flex justify-content-between align-items-center">
        <label for="${rowId}">Receipt No ${nextIndex + 5}</label>
        <button type="button" class="btn btn-link text-danger p-0 remove-dynamic-receipt">Remove</button>
      </div>
      <select name="${rowId}" class="form-control receipt-dynamic-select" id="${rowId}"></select>
      <span class="text-danger receipt-error"></span>
    </div>
  `;

  $("#dynamic_receipts_container").append(rowMarkup);
  populateReceiptDropdown(`#${rowId}`, receipts, selectedValue || selectedReceiptNumber);

  const $newSelect = $(`#${rowId}`);
  $newSelect.rules("add", {
    alphanum_special: true,
    maxlength: 100,
    receiptDuplicate: true,
    validReceiptSelection: true,
  });

  refreshReceiptOptionStates();
}// Duplicate addReceiptRow removed — single implementation later in file is used.

$(document)
  .off("change.salesReceipts", "select[name^='receipt_no'], select[name^='receipt_extra_']")
  .on("change.salesReceipts", "select[name^='receipt_no'], select[name^='receipt_extra_']", function () {
    refreshReceiptOptionStates();
  });

$(document)
  .off("click.salesReceipts", "#addReceiptBtn")
  .on("click.salesReceipts", "#addReceiptBtn", function () {
    addReceiptRow();
  });

$(document)
  .off("click.salesReceipts", ".remove-dynamic-receipt")
  .on("click.salesReceipts", ".remove-dynamic-receipt", function () {
    $(this).closest(".dynamic-receipt-row").remove();
    refreshReceiptOptionStates();
  });

function loadDynamicReceipts(receiptsList) {
  console.log("Loading dynamic receipts from list:", receiptsList);
  const parsedList = parseReceiptsList(receiptsList);
  parsedList.forEach(function (receipt) {
    console.log("Loading receipt into dynamic row:", receipt , "with number", receipt.receipt_number , "and id", receipt.id);
    addReceiptRow(receipt.id, receipt.receipt_number);
  });
}

function initializeDynamicReceipts() {
  refreshReceiptOptionStates();
  syncReceiptsListField();
  try {
    const receiptsListVal = $("#receipts_list").val();
    if (receiptsListVal && receiptsListVal !== '[]') {
      loadDynamicReceipts(receiptsListVal);
    }
  } catch (e) {
    console.warn('initializeDynamicReceipts: failed to load dynamic receipts', e);
  }
}
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
  let headingText =
    (type ? type[0].toUpperCase() + type.slice(1) : "") + " Sales Deals";
  $("#saleheading").text(headingText);
});

$(document).ready(function () {
  console.log(getTypeFromURL());
  const table = $("#myTable").DataTable({
    scrollY: "400px",
    scrollX: true,
    scrollCollapse: true,
    fixedColumns: true,
    paging: true,
    processing: true,
    searching: true,
    language: {
    paginate: {
      previous: "Previous",
      next: "Next "
    }
  },

  pagingType: "simple_numbers",
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
       error: function (xhr, status, error) {
      console.log("entered the error file")
            if (xhr.status === 403) {
                // Option 1: redirect to your custom 403 page
                window.location.href = "/forbidden_page/";

                // Option 2: show SweetAlert (if you’re using it)
                // Swal.fire({
                //     icon: "error",
                //     title: "Access Denied",
                //     text: "You do not have permission to view this page."
                // });
            } else {
                console.error("❌ AJAX Error:", status, error);
            }
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
    "aLengthMenu": [[10,25, 50, 75,100, -1], 
        [10,25, 50, 75,100, "All"]],
        dom:  "<'row mt-1'l<'col-md-6 d-flex align-items-start pl-0'B><'col-md-6 text-end'f>>" +
  "<'row mt-1'<'col-sm-12'tr>>" +
  "<'row mt-1'<'col-md-6'i><'col-md-6 text-end'p>>",
       buttons: [
            {
                extend: 'excelHtml5',
                text: ' Excel',
                titleAttr: 'Excel',
                orientation: 'landscape',
                pageSize: 'A4',
            },
            {
                extend: 'pdfHtml5',
                text: ' PDF',
                columns: [2,3,4,5,6,7,8,9],
                titleAttr: 'PDF',
                orientation: 'landscape',
                pageSize: 'A4',
            },
            
             
        ],

    success: function (data) {
      console.log("✅ Success:", data);
    }, 
    columns: [

      {data:"action", title: "Actions"  },
      
      { data: "email", title: "Submitted By User" },
      { data: "reference_number", title: "Reference Number" },
      {
        data: "date",
        title: "Deal Date",
        render: function (data) {
          return new Date(data).toLocaleDateString(); // Format date
        },
      },
      { data: "unit_details", title: "Unit No" },

      { data: "builduing_name", title: "Building Name" },
      { data: "project_name", title: "Project Name" },
      { data: "deal_amount", title: "Selling Price" },
      {
        data: "submitted_date",
        title: "Submitted Date",
        render: function (data) {
          if (data){
          return new Date(data).toLocaleDateString(); // Format date
          }
          else{
            return "";
          }
        },
      },
      {
        data: "re_submitted_date",
        title: "RE Submitted Date",
        render: function (data) {
          if (data){
          return new Date(data).toLocaleDateString(); // Format date
          }
          else{
            return "";
          }
        },
      },
       // ===================== 🧾 DEAL INFO =====================
  { data: "form_status", title: "Form Status", visible: false },
  // { data: "is_deleted", title: "Is Deleted", visible: false },
  { data: "is_approved_rejected_display", title: "Approval Status", visible: false },
  // { data: "manager_approved_rejected", title: "Manager Approve/Reject", visible: false },
  { data: "approved_rejected_by", title: "Approved/Rejected By", visible: false },
  { data: "created_at", title: "Deal Created At", visible: false },
  { data: "created_by", title: "Deal Created By", visible: false },
  { data: "updated_by", title: "Deal Updated By", visible: false },

  // ===================== 🧍 SELLER DETAILS =====================
  { data: "seller_name", title: "Seller Name", visible: false },
  { data: "seller_source", title: "Seller Source", visible: false },
  { data: "selller_mobile", title: "Seller Mobile", visible: false },
  { data: "seller_email", title: "Seller Email", visible: false },
  { data: "seller_nationality", title: "Seller Nationality", visible: false },

  // Seller Agency
  { data: "seller_agency", title: "Seller Agency", visible: false },
  { data: "seller_agent_name", title: "Seller Agent Name", visible: false },
  { data: "seller_agent_phone", title: "Seller Agent Phone", visible: false },
  { data: "seller_agent_email", title: "Seller Agent Email", visible: false },
  { data: "seller_agency_brn", title: "Seller Agency BRN", visible: false },

  // ===================== 👥 BUYER DETAILS =====================
  { data: "buyer_name", title: "Buyer Name", visible: false },
  { data: "buyer_source", title: "Buyer Source", visible: false },
  { data: "buyer_mobile", title: "Buyer Mobile", visible: false },
  { data: "buyer_email", title: "Buyer Email", visible: false },
  { data: "buyer_nationality", title: "Buyer Nationality", visible: false },

  // Buyer Agency
  { data: "buyer_agency", title: "Buyer Agency", visible: false },
  { data: "buyer_agent_name", title: "Buyer Agent Name", visible: false },
  { data: "buyer_agent_phone", title: "Buyer Agent Phone", visible: false },
  { data: "buyer_agent_email", title: "Buyer Agent Email", visible: false },
  { data: "buyer_agency_brn", title: "Buyer Agency BRN", visible: false },

  // ===================== 🏢 MEDIATING AGENCY =====================
  { data: "mediating_agency", title: "Mediating Agency", visible: false },
  { data: "mediating_agent_name", title: "Mediating Agent Name", visible: false },
  { data: "mediating_agent_phone", title: "Mediating Agent Phone", visible: false },
  { data: "mediating_agent_email", title: "Mediating Agent Email", visible: false },
  { data: "mediating_agency_brn", title: "Mediating Agency BRN", visible: false },

  // ===================== 💰 COMMISSION DETAILS =====================
  { data: "total_commission", title: "Total Commission", visible: false },
  { data: "less_outsude_commission", title: "Less Outside Commission", visible: false },
  { data: "net_commission", title: "Net Commission", visible: false },
  { data: "classic", title: "Classic", visible: false },
  { data: "agent1", title: "Agent1", visible: false },
  { data: "agent2", title: "Agent2", visible: false },
  { data: "agent3", title: "Agent3", visible: false },
  { data: "agent_name1_display", title: "Agent 1 Name", visible: false },
  { data: "agent_name2_display", title: "Agent 2 Name", visible: false },
  { data: "agent_name3_display", title: "Agent 3 Name", visible: false },

  // ===================== 🧾 FINANCE & STATUS =====================
  { data: "receipt_no", title: "Receipt No", visible: false },
  { data: "kyc_number", title: "KYC Number", visible: false },
  { data: "is_sale_aml", title: "AML", visible: false },
  { data: "is_entered_in_finance_system_display", title: "Entered in Finance System", visible: false },
  { data: "agent_comment", title: "Comments by Agent", visible: false },
  { data: "comments", title: "Comments by Admin", visible: false },
  { data: "comments_finance", title: "Comments by Finance", visible: false },






    ],
  });
  $('#filterForm').on('submit', function (e) {
    e.preventDefault(); // Prevent page reload
    table.ajax.reload(); // Reload DataTable with new filters
  });

});

// form search 
  

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
//  
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

// update the single field Finace or comment _finace

//  edit Is entered  finace ststus  or not
function enterInFinance(id) {
  console.log("Updating finance status for ID:", id);
  $.ajax({
    url: "/sales-deals/update-single-field/",
    method: "PUT",
    contentType: "application/json",
    dataType: "json",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"), // if CSRF is enabled
    },
    data: JSON.stringify({
      object_id: id,
      field_name: "is_entered_in_finance_system",
      value: "1",
    }),
    success: function (response) {
      console.log("Update success:", response);
      document.getElementById('financeStatus').textContent = "Yes";

      // ✅ Hide the button
      const btn = document.getElementById(`financeBtn${id}`);
      console.log("Button to hide:", btn);
      if (btn) {
        console.log("Hiding button:", btn);
        btn.style.display = "none";
      }
      // Update UI here, like hiding a button or showing "Yes"
    },
    error: function (xhr, status, error) {
      console.error("Update failed:", xhr.responseText);
    },
  });
}

//  edit finace comment  in the latest data

$(document).on("click", ".editComment", function () {
  // Show the textarea and submit button
  $(".edit_comments_finance").removeAttr("hidden");

  // Load existing comment (if any) into textarea
  const existingComment = $("#existing_comment").text().trim();
  $("#comments_finance").val(existingComment);

  $("#existing_comment").hide();

  // Hide the "Edit/Add Comment" button
  $(this).hide();
});

function comment_finance(id) {
  // e.preventDefault(); // Prevent normal form submit

  const comment = $("#comments_finance").val();

  $.ajax({
    url: "/sales-deals/update-single-field/", // Your backend URL
    method: "PUT",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"), // if CSRF is enabled
    },
    contentType: "application/json",
    data: JSON.stringify({
      object_id: id,
      field_name: "comments_finance",
      value: comment,
    }),
    success: function (response) {
      // Show the label again
      const latestComment = response.updated_value;
      $("#existing_comment").text(latestComment).show(); // Update label text
      $("#existing_comment_label").show();

      // Hide the textarea section
      $(".edit_comments_finance").attr("hidden", true);

      // Optionally, show the button again as "Edit Comment"
      $(".editComment")
        .val("Edit Comment")
        .data("existing-comment", comment)
        .show();
      // location.reload();
      alert("Submiteed the fiance comment");
    },
    error: function (xhr) {
      alert("Failed to save comment.");
    },
  });
}

// edit the deal of sales

$(document).ready(function () {
  const dealId = $("#dealMeta").data("deal-id");

  if (!dealId) {
    console.error("Missing deal ID.");
    return;
  }

  console.log("Editing deal:", dealId);

  // 🔹 Load data via GET
  $.ajax({
    url: `/api/sales-deals/update/${dealId}/`,
    method: "GET",
    success: function (data) {
      console.log("API data:", data);
      const awsUrl = window.awsUrl; // Ensure awsUrl is defined globally
      const referenceNumber = data.reference_number;

      datepickershow_edit();
      
      

      $.each(data, function (key, value) {
        const $field = $(`[name="${key}"], #${key}`);

        if (key === "receipts_list") {
          console.log("Loading receipts_list into dynamic fields:", value);

          $("#receipts_list").val(value); // Set hidden field for receipts_list)

          console.log("Set #receipts_list value:", $("#receipts_list").val());
          
          // return; // skip further processing for this field
        }

        if ($field.length) {
          const type = $field.attr("type");

          // 🔸 Handle file inputs
          if (type === "file") {
            console.log("Handling file input:", key, value);
            renderFilePreviewsNextToInput(key, value, awsUrl, referenceNumber);
            const count = value
              ? value.split(",").filter((f) => f.trim() !== "").length
              : 0;
            appendHiddenFileTrackingFields(key, value || "", count);
            return; // skip .val() on file inputs
          }

          // ✅ Handle radio buttons only
          if ($field.is(":radio")) {
            const $radios = $(`input[type="radio"][name="${key}"]`);
            if (!value || value === "P") {
              $radios.prop("checked", false); // uncheck if P/null
            } else {
              const $match = $radios.filter(`[value="${value}"]`);
              if ($match.length) {
                console.log($match.length);
                $radios.prop("checked", false); // clear others
                $match.prop("checked", true); // set correct one
              } else {
                $radios.prop("checked", false); // no match, clear all
              }
            }

            // ✅ Handle checkboxes
          } else if (type === "checkbox") {
            $field.prop(
              "checked",
              value === true || value === 1 || value === "true"
            );

            // ✅ Handle selects
          } else if ($field.is("select")) {
            $field.val(value).trigger("change");

            // ✅ Handle all other input types
          }
          
          
          else {
            $field.val(value);
          }
          
        }
      });

      // ✅ Manually uncheck specific radio groups (overrides)

      loadAgentDropdown(data);
      loadReceiptDropdown(data);
      // loadDynamicReceipts(data.receipts_list);
      // initializeDynamicReceipts();
      
    },
    error: function () {
      alert("Failed to load data.");
    },

   
  });

  // 🔹 Submit form via POST
  // $("#create_deal").click(function (e) {
  //   console.log("Submitting form for deal ID:", dealId);
  //   e.preventDefault();
  //   const form = $("#sales_form").get(0);
  //   const $form = $("#sales_form"); // Use the form ID, not the button ID
  //   // Replace with actual form ID (not the button)

  //   const formData = new FormData(form); // Use FormData to handle file uploads

  //   console.log("Form data before submission:", formData);

  //   const amlCheckbox = $form.find("input[name='is_sale_aml']")[0];
  //   if (amlCheckbox) {
  //     const value = amlCheckbox.checked ? "Yes" : "No";
  //     formData.set("is_sale_aml", value);
  //     console.log("✅ is_sale_aml sending:", value);
  //   } else {
  //     console.warn("⚠️ Checkbox is_sale_aml not found in form!");
  //   }
  //   // Include checkbox values manually
  //   $form.find("input[type=checkbox]").each(function () {
  //     const fieldName = this.name;
  //     if (fieldName === "is_sale_aml") {
  //       formData.set(fieldName, this.checked ? "Yes" : "No");
  //     } else {
  //       // Default fallback: true/false as strings
  //       formData.set(fieldName, this.checked ? "true" : "false");
  //     }
  //     console.log(`${fieldName} = ${formData.get(fieldName)}`);
  //   });

  //   $.ajax({
  //     url: `/api/sales-deals/update/${dealId}/`,
  //     method: "PUT",
  //     data: formData,
  //     processData: false,
  //     contentType: false,
  //     headers: {
  //       "X-CSRFToken": getCookie("csrftoken"),
  //     },

  //     // ✅ Required to send FormData

  //     success: function (data) {
  //       // $("#save_draft_deal").removeAttr("disabled");
  //       console.log(data.status);
  //        scrollTop();
  //           $("#alert-primary").text("Rental Deal Updated Successfully");
  //             $("#successmsg").show();
  //              setTimeout(function () {
  //               window.location.href = "/rental-deals/approved/" ;
  //             }, 5000);
  //      alert("Rental deal updated successfully!");

  //       if (data.status === "success") {
  //         alert("Rental deal updated successfully!");
  //         location.reload(); // Or redirect if needed
  //       }
  //     },

  //     error: function (err) {
  //       if (err.status === 400) {
  //         const data = err.responseJSON;
  //         let messages = "";

  //         $.each(data, function (field, errors) {
  //           const msg = Array.isArray(errors) ? errors[0] : errors;
  //           messages += `${field}: ${msg}\n`;

  //           $.each(data.data, function (index, value) {
  //             messages +=
  //               index.charAt(0).toUpperCase() +
  //               index.slice(1) +
  //               " : " +
  //               value +
  //               "\n";
  //           });

  //           swal("Please fill mandatory field", messages);

  //           // Show field-wise error messages
  //           $.each(data.data, function (key, val) {
  //             $("#" + key + "_error")
  //               .text(val[0])
  //               .show();

  //             $(document).on("keyup", "input[name='" + key + "']", function () {
  //               $("#" + key + "_error").hide();
  //             });

  //             $(document).on(
  //               "change",
  //               "select[name='" + key + "']",
  //               function () {
  //                 $("#" + key + "_error").hide();
  //               }
  //             );
  //           });
  //         });
  //       } else {
  //         const alertmsg = data.message || "Something went wrong!";
  //         swal("Error", alertmsg, "error");
  //       }
  //       // alert("Update failed.");
  //       console.error(err);
  //     },
  //   });
  // });
});

function scrollTop() {
  $("html, body").animate(
    {
      scrollTop: $(".main-header").offset().top,
    },
    1000
  );
}

function loadAgentDropdown(requestdata) {
  agents = sales_data.agents;
  console.log(agents);

  populateAgentDropdown(
    "#submitted_by_agent",
    agents,
    requestdata.submitted_by_user
  );
  populateAgentDropdown("#agent_name1", agents, requestdata.agent_name1);
  populateAgentDropdown("#agent_name2", agents, requestdata.agent_name2);
  populateAgentDropdown("#agent_name3", agents, requestdata.agent_name3);
}

// populate the user data based on requriement

function populateAgentDropdown(selector, data, selectedId = null) {
  const $dropdown = $(selector);
  $dropdown.empty().append('<option value="">Select Agent</option>');

  data.forEach(function (agent) {
    const isSelected = selectedId == agent.id ? "selected" : "";

    if (isSelected) {
      console.log(
        "agent afterslection",
        selectedId,
        agent.id
      );
    }

    $dropdown.append(
      `<option value="${agent.id}" ${isSelected}>${agent.name}</option>`
    );
  });
}

function loadReceiptDropdown(requestdata) {
  receipts = sales_data.receipts;
  $("#dynamic_receipts_container").empty();

  populateReceiptDropdown("#receipt_no", receipts, requestdata.receipt_no);
  console.log(requestdata.receipt_no);
  console.log("loaded the receipts");
  // Add more dropdowns if needed, e.g.:
  // populateReceiptDropdown("#other_receipt", receipts, requestdata.other_receipt);

  populateReceiptDropdown("#receipt_no2", receipts, requestdata.receipt_no2);
  populateReceiptDropdown("#receipt_no3", receipts, requestdata.receipt_no3);
  populateReceiptDropdown("#receipt_no4", receipts, requestdata.receipt_no4);
  populateReceiptDropdown("#receipt_no5", receipts, requestdata.receipt_no5);

  const selectedReceipts = parseReceiptsList(requestdata.receipts_list);
  const fixedReceiptTokens = [
    requestdata.receipt_no,
    requestdata.receipt_no2,
    requestdata.receipt_no3,
    requestdata.receipt_no4,
    requestdata.receipt_no5,
  ]
    .map(function (value) {
      return String(value || "").trim();
    })
    .filter(function (value) {
      return value.length > 0;
    });

  selectedReceipts
    .filter(function (item) {
      const itemId = String(item.id || "").trim();
      const itemNumber = String(item.receipt_number || "").trim();
      console.log("Checking receipt", itemId, itemNumber, "against fixed tokens", fixedReceiptTokens);
      return (
        !fixedReceiptTokens.includes(itemId) &&
        !fixedReceiptTokens.includes(itemNumber)
      );
    })
    .forEach(function (item) {
      addReceiptRow(item.id, item.receipt_number);
    });

  refreshReceiptOptionStates();
  syncReceiptsListField();
}

// Helper function to populate the receipt dropdown
function populateReceiptDropdown(selector, data, receiptno_from_request) {
  console.log(selector, "receipt selector");
  console.log(data, "receipt data");
  console.log(receiptno_from_request, "receipt number from request");
  const $dropdown = $(selector);
  $dropdown.empty().append('<option value="">Select Receipt</option>');

  const normalizedSelectedValue = String(receiptno_from_request || "").trim();
  let matchedReceiptId = "";


   const noCommissionSelected =
    receiptno_from_request === "No Commission" ? "selected" : "";
  $dropdown.append(
    `<option value="No Commission" ${noCommissionSelected}>No Commission</option>`
  );

  // Add "Null" option
  const nullSelected = receiptno_from_request === "Null" ? "selected" : "";
  $dropdown.append(
    `<option value="Null" ${nullSelected}>Null</option>`
  );

  data.forEach(function (receipt) {
    const isSelected =
      normalizedSelectedValue === String(receipt.id) ||
      normalizedSelectedValue === String(receipt.receipt_number)
        ? "selected"
        : "";

    if (isSelected) {
      matchedReceiptId = String(receipt.id);
    }

    if (isSelected) {
      console.log(
        "receipt afterslection",
        receiptno_from_request,
        receipt.receipt_number
      );
    }

    $dropdown.append(
      `<option value="${receipt.id}" ${isSelected}>${receipt.receipt_number}</option>`
    );
  });

  if (normalizedSelectedValue) {
    if (
      normalizedSelectedValue === "No Commission" ||
      normalizedSelectedValue === "Null"
    ) {
      $dropdown.val(normalizedSelectedValue);
    } else if (matchedReceiptId) {
      $dropdown.val(matchedReceiptId);
    }
  }
}

// ===================== Dynamic Receipts Functions =====================

function parseReceiptsList(receiptsListValue) {
  if (!receiptsListValue) {
    return [];
  }

  if (Array.isArray(receiptsListValue)) {
    return receiptsListValue;
  }

  try {
    const parsedValue = JSON.parse(receiptsListValue);
    return Array.isArray(parsedValue) ? parsedValue : [];
  } catch (error) {
    console.warn("Unable to parse receipts_list", error);
    return [];
  }
}

function getReceiptSelects() {
  return $("select[name^='receipt_no'], select[name^='receipt_extra_']");
}

function getDynamicReceiptSelects() {
  return $("select[name^='receipt_extra_']");
}

function getReceiptNumberFromId(receiptId) {
  const receipt = (sales_data.receipts || []).find(function (item) {
    return String(item.id) === String(receiptId);
  });

  return receipt ? receipt.receipt_number : "";
}

function collectSelectedReceipts() {
  const selectedReceipts = [];
  const seenIds = new Set();

  getDynamicReceiptSelects().each(function () {
    const value = String($(this).val() || "").trim();

    if (!value || !/^\d+$/.test(value) || seenIds.has(value)) {
      return;
    }

    const receiptNumber = getReceiptNumberFromId(value);
    if (!receiptNumber) {
      return;
    }

    selectedReceipts.push({
      id: parseInt(value, 10),
      receipt_number: receiptNumber,
    });
    seenIds.add(value);
  });

  return selectedReceipts;
}

function syncReceiptsListField() {
  const selectedReceipts = collectSelectedReceipts();
  $("#receipts_list").val(JSON.stringify(selectedReceipts));
  return selectedReceipts;
}

function syncReceiptsList() {
  return syncReceiptsListField();
}

function refreshReceiptOptionStates() {
  const receiptSelects = getReceiptSelects();
  const selectedIds = receiptSelects
    .map(function () {
      return String($(this).val() || "").trim();
    })
    .get()
    .filter(function (value) {
      return /^\d+$/.test(value);
    });

  receiptSelects.each(function () {
    const currentValue = String($(this).val() || "").trim();

    $(this)
      .find("option")
      .each(function () {
        const optionValue = String($(this).val() || "").trim();

        if (!/^\d+$/.test(optionValue)) {
          $(this).prop("disabled", false);
          return;
        }

        const shouldDisable =
          selectedIds.includes(optionValue) && optionValue !== currentValue;
        $(this).prop("disabled", shouldDisable);
      });
  });

  refreshAddReceiptButtonState();
  syncReceiptsListField();
}

function refreshAddReceiptButtonState() {
  const receiptSelects = getReceiptSelects();
  const allFilled =
    receiptSelects.length > 0 &&
    receiptSelects.toArray().every(function (field) {
      const value = String($(field).val() || "").trim();
      if (!value) return false;
      if (value === "Null") return false;
      if (value === "No Commission" || value === "No Commision") return false;
      return /^\d+$/.test(value);
    });

  $("#addReceiptBtn").prop("disabled", !allFilled);
}

function addReceiptRow(selectedValue = "", selectedReceiptNumber = "") {
  const nextIndex = $(".dynamic-receipt-row").length + 1;
  const rowId = `receipt_extra_${nextIndex}`;
  const rowMarkup = `
    <div class="col-md-6 mb-2 dynamic-receipt-row" data-row-index="${nextIndex}">
      <div class="d-flex justify-content-between align-items-center">
        <label for="${rowId}">Receipt No ${nextIndex + 5}</label>
        <button type="button" class="btn btn-link text-danger p-0 remove-dynamic-receipt">Remove</button>
      </div>
      <select name="${rowId}" class="form-control receipt-dynamic-select" id="${rowId}"></select>
      <span class="text-danger receipt-error"></span>
    </div>
  `;

  $("#dynamic_receipts_container").append(rowMarkup);
  console.log("Adding receipt row with ID:", rowId, "and selected value:", selectedValue,receipts);
  populateReceiptDropdown(`#${rowId}`, receipts, selectedValue || selectedReceiptNumber);

  const $newSelect = $(`#${rowId}`);
  $newSelect.rules("add", {
    alphanum_special: true,
    maxlength: 100,
    receiptDuplicate: true,
    validReceiptSelection: true,
  });

  refreshReceiptOptionStates();
}

$(document)
  .off("change.salesReceipts", "select[name^='receipt_no'], select[name^='receipt_extra_']")
  .on("change.salesReceipts", "select[name^='receipt_no'], select[name^='receipt_extra_']", function () {
    refreshReceiptOptionStates();
  });

$(document)
  .off("click.salesReceipts", "#addReceiptBtn")
  .on("click.salesReceipts", "#addReceiptBtn", function () {
    addReceiptRow();
  });

$(document)
  .off("click.salesReceipts", ".remove-dynamic-receipt")
  .on("click.salesReceipts", ".remove-dynamic-receipt", function () {
    $(this).closest(".dynamic-receipt-row").remove();
    refreshReceiptOptionStates();
  });

function loadDynamicReceipts(receiptsList) {
  console.log("Loading dynamic receipts from list:", receiptsList);
  const parsedList = parseReceiptsList(receiptsList);

  parsedList.forEach(function (receipt) {
    console.log("Loading dynamic receipt:", receipt, "into form" ,receipt.id ,receipt.receipt_number) ;
    addReceiptRow(receipt.id, receipt.receipt_number);
  });
}

function initializeDynamicReceipts() {
  refreshReceiptOptionStates();
  syncReceiptsListField();
  console.log("Initializing dynamic receipts with current list value:", $("#receipts_list").val());
  loadDynamicReceipts($("#receipts_list").val());
}

// ===================== End Dynamic Receipts Functions =====================

// Function to render file previews next to the input field
// This function assumes you have a file input with the given fieldName
function renderFilePreviewsNextToInput(
  fieldName,
  fileString,
  awsUrl,
  referenceNumber
) {
  const $input = $(`#${fieldName}`);
  $input.siblings(".upload_prev").remove(); // Clear previous previews

  console.log("Rendering file previews for:", fieldName);
  console.log("File string:", fileString);
  console.log("AWS URL:", awsUrl);
  console.log("Reference number:", referenceNumber);

  const files = (fileString || "")
    .split(",")
    .map((f) => f.trim())
    .filter((f) => f !== "");
  console.log("Files to preview:", files);
  files.forEach((fileName, index) => {
    const fileUrl = `${awsUrl}${referenceNumber}/${fileName}`;
    const label = `${fieldName} ${index + 1}`;

    const preview = `
      <div class="upload_prev">
        <a href="${fileUrl}" target="_blank">${label}</a>
        <p class="remove_file" id="${fileName}" data-name="${fieldName}" data-existing="old">X</p>
      </div>`;
    $input.after(preview);
  });
}

// Function to append hidden fields for tracking file uploads
// This function creates hidden fields to track existing files, removed files, and new removed count
function appendHiddenFileTrackingFields(
  fieldName,
  existingValue = "",
  count = 0
) {
  const $input = $(`#${fieldName}`);
  $(`#${fieldName}_existing_count,
     #${fieldName}_existing_values,
     #${fieldName}_removed,
     #${fieldName}_new_removed_count`).remove(); // remove if already added

  const hidden = `
    <input type="hidden" id="${fieldName}_existing_count" name="${fieldName}_existing_count" value="${count}">
    <input type="hidden" id="${fieldName}_existing_values" name="${fieldName}_existing_values" value="${existingValue}">
    <input type="hidden" id="${fieldName}_removed" name="${fieldName}_removed"  >
    <input type="hidden" id="${fieldName}_new_removed_count" name="${fieldName}_new_removed_count" >
    <div id="upload_prevss" class="${fieldName}_list"></div>
  `;
  $input.after(hidden);
}

// File input change handler
$('input[type="file"]').on("change", function () {
  const input = this;
  var namedata = $(this).attr("id");
  $("." + namedata + "_list").empty();
  $("#" + namedata + "_new_removed_count").val(this.files.length);

  const file = input.files[0];
  if (!file) return;

  if (this.files.length > 0) {
    var filename = this.files[0].name;
    var lastIndex = filename.lastIndexOf("\\");
    console.log("Last index of backslash:", lastIndex);
    if (lastIndex >= 0) {
      filename = filename.substring(lastIndex + 1);
    }

    filesize = 0;
    var fileCount = 4;
    if ($("#" + $(this).attr("id") + "_existing_count").val()) {
      fileCount =
        fileCount -
        parseInt($("#" + $(this).attr("id") + "_existing_count").val());
    }

    files = this.files;
    var result_array = Array.from(files);
    var added = false;
    for (let i = 0; i < this.files.length; i++) {
      filesize = parseFloat(filesize + this.files[i].size);
      var name = files[i].name;
      console.log("File name:", name);
      console.log("File size:", this.files[i].size);
      extension = "." + (filename.split('.').pop().toLowerCase());

      var validNamePattern =  /^[a-zA-Z0-9 ._()-]+$/;
;
        if (!validNamePattern.test(filename)) {
            $("#" + $(this).attr("id") + "_error")
              .html("File name contains invalid characters. Allowed: letters, numbers, ., _, -")
              .show();
            $("#" + $(this).attr("id")).val("");
            $("." + namedata + "_list").empty();
            $("#" + namedata + "_new_removed_count").val("0");
            
        }



          if (
            extension != ".pdf" &&
            extension != ".jpg" &&
            extension != ".jpeg" &&
            extension != ".png"
          ) {
            $("#" + $(this).attr("id") + "_error")
              .html("Only pdf, jpg, jpeg, png files are allowed")
              .show();
            $("#" + $(this).attr("id")).val("");
            $("." + namedata + "_list").empty();
            $("#" + namedata + "_new_removed_count").val("0");
            return false;
          }

      $.map(result_array, function (name) {
        if (name !== filename) {
          var added = true;
        }
      });
      if (!added) {
        console.log("File already exists in the list, skipping:", filename);
        $('.'+namedata+'_list').append('<div class="upload_prev">'+'<a class="filenameupload">'+this.files[i].name+'</a>'+'<p class="remove_file" id="'+this.files[i].name+'" data-name="'+namedata+'"'+'>X</p></div>');
      }
    }
    if (filesize / 1024 / 1024 > 3) {
      $("#" + $(this).attr("id") + "_error")
        .html("File size should be less than 3 mb")
        .show();
      $("#" + $(this).attr("id")).val("");
      $("." + namedata + "_list").empty();
      $("#" + namedata + "_new_removed_count").val("0");
    } else if (this.files.length > fileCount) {
      alert("Length exceeded. Please select no more than 4 files");
      $("#" + $(this).attr("id")).val("");
      $("." + namedata + "_list").empty();
      $("#" + namedata + "_new_removed_count").val("0");
    } else {
      $("#yt" + $(this).attr("id")).val("true");
      $("#" + $(this).attr("id") + "_error")
        .html("")
        .hide();
      $("#" + $(this).attr("id") + "-error")
        .html("")
        .hide();
    }
  }
});

// Remove file handler
$(document).on("click", ".remove_file", function () {
  var name = $(this).data("name");
  console.log(name);
  var value = $(this).attr("id");
  var existingType = $(this).data("existing");
  if ($("#" + name + "_removed").val().length == 0) {
    $("#" + name + "_removed").val(value);
  } else {
    $("#" + name + "_removed").val(
      $("#" + name + "_removed").val() + ", " + value
    );
  }
  if (existingType == "old") {
    $("#" + name + "_existing_count").val(
      parseInt($("#" + name + "_existing_count").val()) - 1
    );
  } else {
    $("#" + name + "_new_removed_count").val(
      parseInt($("#" + name + "_new_removed_count").val()) - 1
    );
  }

  const input = document.getElementById(name);
  const dt = new DataTransfer();
  const files = input.files;

  for (let i = 0; i < files.length; i++) {
    if (files[i].name !== value) {
      dt.items.add(files[i]); // keep only files not being removed
    }
  }

  input.files = dt.files;

  $(this).parent("div").remove();
  $(this).parents("span").remove();
});

function datepickershow_edit() {
  $("#date").datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "-100:+0",
    maxDate: 0,
  });

  $("#deal_start_date").datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "-100:+0",
    maxDate: 0,
    onSelect: function (date) {
      var date2 = $("#deal_start_date").datepicker("getDate");
      $("#deal_end_date").datepicker("option", "minDate", date2);
      appendDate(); // optional
      $("#deal_end_date").datepicker("option", "yearRange", "-100:+10");
    },
  });

  $("#deal_end_date").datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true,
    onClose: function () {
      var dt1 = $("#deal_start_date").datepicker("getDate");
      var dt2 = $("#deal_end_date").datepicker("getDate");
      if (dt2 <= dt1) {
        var minDate = $("#deal_end_date").datepicker("option", "minDate");
        $("#deal_end_date").datepicker("setDate", minDate);
      }
    },
  });

  console.log("Date selected.");
}

$.validator.addMethod(
  "alphanum_special",
  function (value, element) {
    const cleaned = value.trim();
    return this.optional(element) || /^[a-zA-Z0-9 _.,\-\/()]*$/.test(cleaned);
  },
  "Only alphanumeric and basic special characters allowed."
);

$.validator.addMethod(
  "phoneNumber",
  function (value, element) {
    var exp = /^[\+]?\d*$/im;
    //console.log(exp.test(value));
    return exp.test(value);
  },
  "Phone number must only contain numbers and +"
);

$.validator.addMethod(
  "numeric",
  function (value, element, param) {
    return this.optional(element) || /^[-]?[0-9-., ]+$/.test(value);
  },
  "Enter only numbers."
);

$.validator.addMethod(
  "only_text",
  function (value, element) {
    return this.optional(element) || /^[a-zA-Z\s]+$/.test(value.trim());
  },
  "Only letters and spaces are allowed."
);
// validations for the form
$.validator.addMethod(
  "custom_email",
  function (value, element) {
    // Accepts empty values or valid email format
    return (
      this.optional(element) ||
      /^[\w\.\-]+@([\w\-]+\.)+[a-zA-Z]{2,7}$/.test(value.trim())
    );
  },
  "Please enter a valid email address."
);

$.validator.addMethod(
  "only_text",
  function (value, element) {
    return (
      this.optional(element) || value == value.match(/^[ a-zA-Z][ a-zA-Z_/-]*$/)
    );
  },
  "Enter valid Name"
);

$.validator.addMethod(
  "custom_email",
  function (value, element) {
    var regEx =
      /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
    return this.optional(element) || regEx.test(value);
  },
  "Enter a valid email address."
);

$.validator.addMethod(
  "alpha_numeric",
  function (value, element, param) {
    return this.optional(element) || /^[-]?[a-zA-Z0-9]+$/.test(value);
  },
  "Enter valid Profile Id"
);

$.validator.addMethod(
  "numeric",
  function (value, element, param) {
    return this.optional(element) || /^[-]?[0-9-., ]+$/.test(value);
  },
  "Enter only numbers."
);
$.validator.addMethod(
  "text_special",
  function (value, element) {
    return (
      this.optional(element) ||
      value == value.match(/[A-Za-z_~\-!@#'\$%\^&\*\(\)]+$/)
    );
  },
  "Enter only letters and special characters."
);
$.validator.addMethod(
  "alphanum_special",
  function (value, element) {
    return (
      this.optional(element) ||
      value == value.match(/[A-Za-z0-9,.:;_~\-!|@#'’\$%\^&\*\(\)\s/']+$/)
    );
  },
  "Enter only letters, numbers and special characters."
);
$.validator.addMethod(
  "lettersonly",
  function (value, element) {
    return (
      this.optional(element) ||
      /^[a-zA-Z][ a-zA-Z0-9_@,.!$/#&+-]*$/i.test(value)
    );
  },
  "Letters only please"
);

$.validator.addMethod("receiptDuplicate", function (value, element) {
  if (!value) return true;

  var currentValue = value.trim();
  if (!/^\d+$/.test(currentValue)) return true;

  var receipts = $("select[name^='receipt_no'], select[name^='receipt_extra_']")
    .map(function () {
      return {
        id: $(this).attr("id"),
        value: $(this).val()?.trim(),
      };
    })
    .get();

  var currentId = $(element).attr("id");

  for (let i = 0; i < receipts.length; i++) {
    if (
      receipts[i].id !== currentId &&
      /^\d+$/.test(String(receipts[i].value || "").trim()) &&
      receipts[i].value === currentValue
    ) {
      return false;
    }
  }

  return true;
}, "Duplicate receipt number is not allowed.");

$.validator.addMethod("validReceiptSelection", function (value, element) {
  const normalized = String(value || "").trim();
  if (!normalized) return true;
  if (normalized === "Null" || normalized === "No Commission" || normalized === "No Commision") return true;
  return /^\d+$/.test(normalized);
}, "Please select a valid receipt number.");

$("#sales_form").validate({
  rules: {
    submitted_by_agent: {
      required: true,
    },
    unit_details: {
      required: true,
      alphanum_special: true,
      maxlength: 15,
    },
    builduing_name: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    screening: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    deal_amount: {
      numeric: true,
      maxlength: 10,
    },
    seller_name: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    seller_source: {
      required: true,
    },
    selller_mobile: {
      required: true,

      minlength: 6,
      maxlength: 15,
    },
    seller_email: {
      required: true,
      custom_email: true,
      maxlength: 100,
    },
    seller_nationality: {
      required: true,
      maxlength: 100,
    },
    buyer_nationality: {
      required: true,
      maxlength: 100,
    },
    buyer_name: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    buyer_source: {
      required: true,
    },
    buyer_mobile: {
      required: true,

      minlength: 6,
      maxlength: 15,
    },
    buyer_email: {
      required: true,
      custom_email: true,
      maxlength: 100,
    },
    seller_agency: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    seller_agent_name: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    seller_agency_brn: {
      alphanum_special: true,
      maxlength: 255,
    },
    seller_agent_phone: {
      required: true,

      minlength: 6,
      maxlength: 15,
    },
    seller_agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    buyer_agency: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    buyer_agent_name: {
      required: true,
      alphanum_special: true,
      maxlength: 255,
    },
    buyer_agency_brn: {
      alphanum_special: true,
      maxlength: 255,
    },
    buyer_agent_phone: {
      required: true,

      minlength: 6,
      maxlength: 15,
    },
    buyer_agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    project_name: {
      required: true,

      maxlength: 255,
    },
    mediating_agency: {
      alphanum_special: true,
      maxlength: 255,
    },
    mediating_agent_name: {
      alphanum_special: true,
      maxlength: 255,
    },
    mediating_agency_brn: {
      alphanum_special: true,
      maxlength: 255,
    },
    mediating_agent_phone: {
      minlength: 6,
      maxlength: 15,
    },
    mediating_agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    total_commission: {
      required: true,
      numeric: true,
      maxlength: 10,
    },
    less_outsude_commission: {
      required: true,
      alphanum_special: true,
      maxlength: 100,
    },
    net_commission: {
      required: true,
      numeric: true,
      maxlength: 10,
    },
    classic: {
      required: true,
      numeric: true,
      maxlength: 10,
    },
    agent1: {
      required: true,
      numeric: true,
      maxlength: 10,
    },
    agent_name1: {
      required: true,
    },
    agent2: {
      numeric: true,
      maxlength: 10,
    },
    agent3: {
      numeric: true,
      maxlength: 10,
    },
    agent_comment: {
      alphanum_special: true,
      
    },
    comments: {
      alphanum_special: true,
      
    },
    receipt_no: {
      required: true,
      alphanum_special: true,
      maxlength: 100,
      receiptDuplicate: true,
      validReceiptSelection: true,
    },
    
    receipt_no2: {
      alphanum_special: true,
      maxlength: 100,
      receiptDuplicate: true,
      validReceiptSelection: true,
    },
      receipt_no3: {
      alphanum_special: true,
      maxlength: 100,
      receiptDuplicate: true,
      validReceiptSelection: true,
    },
    receipt_no4: {
      alphanum_special: true,
      maxlength: 100,
      receiptDuplicate: true,
      validReceiptSelection: true,
    },
    receipt_no5: {
      alphanum_special: true,
      maxlength: 100,
      receiptDuplicate: true,
      validReceiptSelection: true,
    },

    is_sale_aml: {
      required: true,
    },
    kyc_number: {
      numeric: true,
      maxlength: 45,
    },
  },
  messages: {
    agent1: {
      number: "Enter only Numbers",
    },
    agent2: {
      number: "Enter only Numbers",
    },
    agent3: {
      number: "Enter only Numbers",
    },
  },
  errorPlacement: function (error, element) {
    if (element.attr("type") == "radio") {
      $("#is_sale_aml_error").css("margin-right", "200px");
      error.addClass("field_error");
      error.insertAfter("#is_sale_aml_error");
    } else {
      error.insertAfter(element);
    }
  },
});

$(document).on("click", "#create_deal", function (event) {
  $(
    '[name="submitted_by_agent"],[name="seller_agency"],[name="seller_agent_name"],[name="seller_agent_phone"],[name="buyer_agency"],[name="buyer_agent_name"],[name="buyer_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="agent_name1"],[name="receipt_no"],[name="is_sale_aml"]'
  ).each(function () {
    $(this).rules("add", "required");
  });
  if ($("#sales_form").valid()) {
    $("#save_as").val("update-deal");
    var url = "list/";
    if (
      countMultipleFiles("manager_cheque_copy") &
      countMultipleFiles("owners_passport_copy") &
      countMultipleFiles("old_title_deed") &
      countMultipleFiles("buyers_passport_copy") &
      countMultipleFiles("signed_mou") &
      countMultipleFiles("new_title_deed") &
      countMultipleFiles("screening") &
      countMultipleFiles("title_deed") &
      countMultipleFiles("buyers_deposit_cheque_copy") &
      checkKyc()
    ) {
      updatefunctionality(url);
    }
  } else {
    $("html, body").animate(
      {
        scrollTop: $(".main-header").offset().top,
      },
      1000
    );
       var validator = $("#sales_form").validate();
          showErrors(validator);
  }
});
$(document).on("click", "#update_draft", function (event) {
  $(
    '[name="seller_agency"],[name="seller_agent_name"],[name="seller_agent_phone"],[name="buyer_agency"],[name="buyer_agent_name"],[name="buyer_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="agent_name1"],[name="receipt_no"],[name="is_sale_aml"]'
  ).each(function () {
    $(this).rules("remove", "required");
  });
  if ($("#sales_form").valid() & countMultipleFiles("screening")) {
    var url = "draft/";
    $("#save_as").val("update-draft");
    updatefunctionality(url);
  } else {
    $("html, body").animate(
      {
        scrollTop: $(".main-header").offset().top,
      },
      1000
    );
    var validator = $("#sales_form").validate();
          showErrors(validator);
  }
});
function checkKyc() {
  var result = true;
  $("#sale_kyc_number_error").empty();
  $("#kyc_number_error").empty();
  var existing_count = parseInt($("#sale_kyc_number_existing_count").val());
  var removed_count = parseInt($("#sale_kyc_number_new_removed_count").val());
  if ($("#sale_kyc_number_new_removed_count").val() == "") {
    var removed_count = 0;
  }
  if (existing_count < 1 && removed_count < 1 && $("#kyc_number").val() == "") {
    result = false;
    $("#sale_kyc_number_error")
      .html("Either KYC Form or KYC Number is required!")
      .show();
    $("#kyc_number_error")
      .html("Either KYC Form or KYC Number is required!")
      .show();
  }
  return result;
}
function countMultipleFiles(feild) {
  var result = true;
  if (
    $("#" + feild + "_existing_count").val() < 1 &&
    $("#" + feild + "_new_removed_count").val() < 1
  ) {
    result = false;
    var feildvalue = feild;
    $("#" + feild + "_error")
      .html("This field is required.")
      .show();
  }
  return result;
}
function updatefunctionality(urls) {
  const dealId = $("#dealMeta").data("deal-id");
  const form = $("#sales_form").get(0);
  const $form = $("#sales_form"); // Use the form ID, not the button ID
  // Replace with actual form ID (not the button)

  const formData = new FormData(form); // Use FormData to handle file uploads

  console.log("Form data before submission:", formData);

  const amlCheckbox = $form.find("input[name='is_sale_aml']")[0];
  if (amlCheckbox) {
    const value = amlCheckbox.checked ? "Yes" : "No";
    formData.set("is_sale_aml", value);
    console.log("✅ is_sale_aml sending:", value);
  } else {
    console.warn("⚠️ Checkbox is_sale_aml not found in form!");
  }
  // Include checkbox values manually
  $form.find("input[type=checkbox]").each(function () {
    const fieldName = this.name;
    if (fieldName === "is_sale_aml") {
      formData.set(fieldName, this.checked ? "Yes" : "No");
    } else {
      // Default fallback: true/false as strings
      formData.set(fieldName, this.checked ? "true" : "false");
    }
  });
  $("#create_deal").attr("disabled", true);
  $(".loadscreen").show();
  $("html, body").animate(
    {
      scrollTop: $(".main-header").offset().top,
    },
    1000
  );
  if (document.getElementById("date").disabled == true)
    document.getElementById("date").removeAttribute("disabled");
  $.ajax({
    method: "PUT",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    url: `/api/sales-deals/update/${dealId}/`,
    data: formData,
    contentType: false,
    processData: false,
  }).done(function (data, textStatus, xhr, Response) {
    $(".loadscreen").hide();
    $("#create_deal").removeAttr("disabled", true);
    if (xhr.status == 200) {
      scrollTop();
      $("#alert-primary").text("Sales Deal Updated Successfully");
      $("#successmsg").show();
      $("#sales_form")[0].reset();
      setTimeout(function () {
        if (urls == "list/") {
          window.location.href ="/sales-deals/" + urls;
        } else {
          window.location.href =   document.referrer;
        }
      }, 3000);
    } else if (data.status == "validation_error"  || data.status== 400 ) {
      $.each(data.data, function (key, val) {
        $("#" + key + "_error").text(val[0]);
        $("#" + key + "_error").show();
        $(document).on("keyup", "input[name='" + key + "']", function (e) {
          $("#" + key + "_error").hide();
        });
        $(document).on("change", "select[name='" + key + "']", function (e) {
          $("#" + key + "_error").hide();
        });
      });
    } else {
      if (data.data == "DUF500") {
        $("#alert-primary").text("Document Upload Failed! Please Try Again.");
        $("#successmsg").show();
        setTimeout(function () {
          $("#successmsg").fadeOut();
        }, 3000);
      } else {
        $("#alert-primary").text("Something Went Wrong!");
        $("#successmsg").show();
        setTimeout(function () {
          $("#successmsg").fadeOut();
        }, 3000);
      }
    }
  })
  .fail(function (xhr, textStatus, errorThrown, Response) {
            // This block runs for HTTP error responses (4xx or 5xx status codes)
            console.log("AJAX Request Failed!");
            console.log("HTTP Status Code:", xhr.status);
            console.log("Text Status:", textStatus);
            console.log("Error Thrown:", errorThrown);
            console.log("Error Thrown:", xhr.responseJSON);

            let errorMessage = "An unknown error occurred.";

            if (xhr.status === 400) {
              // This is your "Bad Request" error
              console.log("Bad Request details:", xhr.responseJSON);
              scrollTop();

              // Attempt to extract specific error messages from the backend
              if (xhr.responseJSON) {
                if (typeof xhr.responseJSON === "object") {
                  // If backend sends an object with error details (common in DRF)
                  const errors = [];
                  for (const key in xhr.responseJSON) {
                    if (Object.hasOwnProperty.call(xhr.responseJSON, key)) {
                      const element = xhr.responseJSON[key];
                      if (Array.isArray(element)) {
                        errors.push(`${key}: ${element.join(", ")}`);
                      } else {
                        errors.push(`${key}: ${element}`);
                      }
                    }
                  }
                  errorMessage =  errors.join("; ");
                } else {
                  // If backend sends a simple string message
                  errorMessage =   xhr.responseJSON;
                }
              } else {
                errorMessage = "Bad Request: Invalid data provided.";
              }
            }


            // Display the error message to the user
            // Make sure you have an element with id="alert-danger" in your HTML
            //$("#alert-danger").text(errorMessage).show();

            swal("Please Fill field", errorMessage);
            $("#alert-primary").text(errorMessage);
            $("#successmsg").show();
            setTimeout(function () {
              $("#successmsg").fadeOut();
            }, 3000);

            // Hide error message after a few seconds // Display errors a bit longer
          })
  
  ;
}


var lang = "";
      if (lang == "ar") {
        var oLanguage = "//cdn.datatables.net/plug-ins/1.11.3/i18n/ar.json";
        var msg = "الرجاء ملء الحقل الإلزامي";
      } else {
        var oLanguage = "";
        var msg = "Please fill mandatory field";
      }


  function showErrors(validator) {
        var messages = "";
        console.log(validator, "messages in show errors validator");
        $.each(validator.errorMap, function (index, value) {
          if (lang == "ar") {
            for (var key in form_fields) {
              var val = form_fields[key];

              if (key == index) {
                messages += val + " : " + value + "\n";
              } else {
                 messages += index.charAt(0).toUpperCase() + index.slice(1) + ' : ' + value+'\n';
              }
            }
          } else {
            messages +=
              index.charAt(0).toUpperCase() +
              index.slice(1) +
              " : " +
              value +
              "\n";

              console.log(messages, "messages in show errors else");
          }
        });
        console.log(messages);
        swal(msg, messages);
      }
