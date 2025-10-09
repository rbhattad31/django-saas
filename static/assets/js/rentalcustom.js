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

console.log(currentUser);

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
    url: "/update-single-field/", // Your backend URL
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
    waiting: "waiting-finance",
    rejected: "rejected",
    "entered-finance": "entered-finance",
    "pending-finance": "pending-finance",
  };

  return mapping[lastPart] || null;
}

console.log(getTypeFromURL())

// for the heading  to see all l types 
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
    language: {
    paginate: {
      previous: "Previous",
      next: "Next "
    }
  },

  pagingType: "simple_numbers",
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
                columns: [2,3,4,5,6,7,8,9,10],
                titleAttr: 'PDF',
                orientation: 'landscape',
                pageSize: 'A4',
            },
            
             
        ],
  
    columns: [
     {data: "action",
        title: "Action ",},
      { data: "email", title: "submitted_by_user" },
      {
        data: "reference_number",
        fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
          $(nTd).html(
            `<a href='/rental-deals/view/${oData.id}/' class='anchortag text-black text-decoration-none'>${sData}</a>`
          );
        },
        title: "Reference Number",
      },
      {
        data: "date",
        title: "Deal Date",
        // render: function (data) {
        //   return new Date(data).toLocaleDateString(); // ✅ format: M/D/YYYYsss
        // },
      },

      { data: "unit_details", title: "Unit No" },
      { data: "building_name", title: "Building Name" },

      { data: "project_name", title: "Project Name" },
      { data: "rental_price", title: "Rental Price" },

      {
        data: "deal_start_date",
        title: "Deal Start Date",
        // render: function (data) {
        //   return new Date(data).toLocaleDateString();
        // },
      },

      {
        data: "deal_end_date",
        title: "Deal End Date",
        // render: function (data) {
        //   return new Date(data).toLocaleDateString();
        // },
      },

      {
        data: "submitted_date",
        title: "Submitted Date",
        // render: function (data) {
        //   return new Date(data).toLocaleDateString(); // ✅ format: M/D/YYYY
        // },
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
        $(this).parent("li").addClass("actived");
      }
    });
  }
});


// script to activate delete view

   

  

let selectedDealId = null;

// When user clicks the trash icon — open modal
$(document).on("click", ".delete-btn", function () {
  selectedDealId = $(this).data("id");
  $("#deleteModal").modal("show");
});

// When user confirms delete in modal
$("#confirmDeleteBtn").on("click", function () {
  if (!selectedDealId) return;

  $.ajax({
    url: `/rental-deals/${selectedDealId}/delete/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: function () {
      $("#deleteModal").modal("hide");

      // Refresh DataTable or reload page
      $("#myTable").DataTable().ajax.reload(null, false); // or use location.reload();
    },
    error: function (e) {
      console.log(e);
      alert("Error deleting record");
    },
  });
});

// is entered in finance system
function enterInFinance(id) {
  $.ajax({
    url: "/update-single-field/",
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
      document.getElementById(`financeStatus${id}`).textContent = "Yes";

      // ✅ Hide the button
      const btn = document.getElementById(`financeBtn${id}`);
      if (btn) {
        btn.style.display = "none";
      }
      // Update UI here, like hiding a button or showing "Yes"
    },
    error: function (xhr, status, error) {
      console.error("Update failed:", xhr.responseText);
    },
  });
}

/// handle next and previoues buttons

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

// Handle the click event for the edit button
// This will fetch the deal data and populate the form fields
$(document).ready(function () {
  const dealId = $("#dealMeta").data("deal-id");

  if (!dealId) {
    console.error("Missing deal ID.");
    return;
  }

  console.log("Editing deal:", dealId);

  // 🔹 Load data via GET
  $.ajax({
    url: `/api/rental-deals/update/${dealId}/`,
    method: "GET",
    success: function (data) {
      console.log("API data:", data);
      const awsUrl = window.awsUrl; // Ensure awsUrl is defined globally
      const referenceNumber = data.reference_number;

      datepickershow_edit();
      // loadAgentDropdown(data);
      // loadReceiptDropdown(data);

     $.each(data, function (key, value) {
  const $field = $(`[name="${key}"], #${key}`);

  if ($field.length) {
    const type = $field.attr("type");

    // 🔸 Handle file inputs
    if (type === "file") {
      console.log("Handling file input:", key, value);
      renderFilePreviewsNextToInput(key, value, awsUrl, referenceNumber);
      const count = value ? value.split(",").filter((f) => f.trim() !== "").length : 0;
      appendHiddenFileTrackingFields(key, value || "", count);
      return; // skip .val() on file inputs
    }

    // ✅ Handle radio buttons only
    if ($field.is(':radio')) {
      const $radios = $(`input[type="radio"][name="${key}"]`);
      if (!value || value === "P") {
        $radios.prop("checked", false); // uncheck if P/null
      } else {
        const $match = $radios.filter(`[value="${value}"]`);
        if ($match.length) {
          console.log($match.length)
          $radios.prop("checked", false); // clear others
          $match.prop("checked", true);   // set correct one
        } else {
          $radios.prop("checked", false); // no match, clear all
        }
      }

    // ✅ Handle checkboxes
    } else if (type === "checkbox") {
      $field.prop("checked", value === true || value === 1 || value === "true");

    // ✅ Handle selects
    } else if ($field.is("select")) {
      $field.val(value).trigger("change");

    // ✅ Handle all other input types
    } else {
      $field.val(value);
    }

    loadAgentDropdown(data);
    loadReceiptDropdown(data);
  }
});

// ✅ Manually uncheck specific radio groups (overrides)
 

    },
    error: function () {
      alert("Failed to load data.");
    },
  });

  // 🔹 Submit form via POST

 
}); 

function updatefunctionality(url) {
 

    if ($("#deal_form").valid()) {
    var dealId = $("#dealMeta").data("deal-id");
    console.log("Submitting form for deal ID:", dealId);
    // e.preventDefault();
    const form = $("#deal_form").get(0);
    const $form = $("#deal_form"); // Use the form ID, not the button ID
    // Replace with actual form ID (not the button)

    const formData = new FormData(form); // Use FormData to handle file uploads

    console.log("Form data before submission:", formData);

    const amlCheckbox = $form.find("input[name='is_rental_aml']")[0];
    if (amlCheckbox) {
      const value = amlCheckbox.checked ? "Yes" : "No";
      formData.set("is_rental_aml", value);
      console.log("✅ is_rental_aml sending:", value);
    } else {
      console.warn("⚠️ Checkbox is_rental_aml not found in form!");
    }
    // Include checkbox values manually
    $form.find("input[type=checkbox]").each(function () {
      const fieldName = this.name;
      if (fieldName === "is_rental_aml") {
        formData.set(fieldName, this.checked ? "Yes" : "No");
      } else {
        // Default fallback: true/false as strings
        formData.set(fieldName, this.checked ? "true" : "false");
      }
      console.log(`${fieldName} = ${formData.get(fieldName)}`);
    });

    $.ajax({
      url: `/api/rental-deals/update/${dealId}/`,
      method: "PUT",
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },

      // ✅ Required to send FormData

      success: function (data) {
        // $("#save_draft_deal").removeAttr("disabled");
        console.log(data.status);
         scrollTop();
            $("#alert-primary").text("Rental Deal Updated Successfully");
              $("#successmsg").show();
               setTimeout(function () {
                window.location.href = "/rental-deals/"+url ;
              }, 5000);
      //  alert("Rental deal updated successfully!");

        if (data.status === "success") {
          alert("Rental deal updated successfully!");
          location.reload(); // Or redirect if needed
        }
      },

      error: function (err) {
        if (err.status === 400) {
          const data = err.responseJSON;
          let messages = "";

          $.each(data, function (field, errors) {
            const msg = Array.isArray(errors) ? errors[0] : errors;
            messages += `${field}: ${msg}\n`;

            $.each(data.data, function (index, value) {
              messages +=
                index.charAt(0).toUpperCase() +
                index.slice(1) +
                " : " +
                value +
                "\n";
            });

            swal("Please fill mandatory field", messages);

            // Show field-wise error messages
            $.each(data.data, function (key, val) {
              $("#" + key + "_error")
                .text(val[0])
                .show();

              $(document).on("keyup", "input[name='" + key + "']", function () {
                $("#" + key + "_error").hide();
              });

              $(document).on(
                "change",
                "select[name='" + key + "']",
                function () {
                  $("#" + key + "_error").hide();
                }
              );
            });
          });
        } 
             else if (err.status === 403){
           
      
                // Option 1: redirect to your custom 403 page
                window.location.href = "/forbidden_page/";


        }else {
          const alertmsg = data.message || "Something went wrong!";
          swal("Error", alertmsg, "error");
        }
        // alert("Update failed.");
        console.error(err);
      },
    });

  }
  else{
         const alertmsg = "form Is not valid  ";
          swal("Error", alertmsg, "error");

  }

  

};


function scrollTop() {
        $("html, body").animate(
          {
            scrollTop: $(".main-header").offset().top,
          },
          1000
        );
      }

      
function loadAgentDropdown(requestdata) {
  agents = rental_data.agents;
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
      console.log("agent after selection", selectedId, agent.id);
    }

    $dropdown.append(
      `<option value="${agent.id}" ${isSelected}>${agent.name}</option>`
    );
  });
}
 

function loadReceiptDropdown(requestdata) {
  receipts = rental_data.receipts;

  populateReceiptDropdown("#receipt_no", receipts, requestdata.receipt_no);
  console.log(requestdata.receipt_no);
  console.log("loaded teh reciepts");
  // Add more dropdowns if needed, e.g.:
  // populateReceiptDropdown("#other_receipt", receipts, requestdata.other_receipt);
}

// Helper function to populate the receipt dropdown
function populateReceiptDropdown(selector, data, receiptno_from_request) {
  console.log(selector, "recipt selector");
  console.log(data, "receipt data");
  console.log(receiptno_from_request, "receipt number from request");
  const $dropdown = $(selector);
  $dropdown.empty().append('<option value="">Select Receipt</option>');


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
      receiptno_from_request == receipt.receipt_number ? "selected" : "";
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
}

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

      var validNamePattern = /^[a-zA-Z0-9 ._()-]+$/;
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

   $.validator.addMethod("custom_email", function (value, element) {
      		var regEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
        	return this.optional(element) || regEx.test(value);
    		}, "Enter a valid email address.");

        $.validator.addMethod("alpha_numeric", function (value, element, param) {
              return this.optional(element) || /^[-]?[a-zA-Z0-9]+$/.test(value);
            }, "Enter valid Profile Id");

        $.validator.addMethod("numeric", function (value, element, param) {
              return this.optional(element) || /^[-]?[0-9-., ]+$/.test(value);
            }, "Enter only numbers.");
        $.validator.addMethod("text_special", function(value, element) {
                return this.optional(element) || value == value.match(/[A-Za-z_~\-!@#'\$%\^&\*\(\)]+$/);
            },"Enter only letters and special characters.");
        $.validator.addMethod("alphanum_special", function(value, element) {
            return this.optional(element) || value == value.match(/[A-Za-z0-9,.:;_~\-!|@#'\$%\^&\*\(\)\s/]+$/);
        },"Enter only letters, numbers and special characters.");
        $.validator.addMethod("lettersonly", function(value, element) {
          return this.optional(element) || /^[a-zA-Z][ a-zA-Z0-9_@,.!$/#&+-]*$/i.test(value);
        }, "Letters only please")
         
        $.validator.addMethod(
          "only_text",
          function (value, element) {
            return this.optional(element) || value == value.match(/^[ a-zA-Z][ a-zA-Z_/-]*$/); // Example: allows only letters and spaces
          },
          "Please enter only letters."
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
$("#deal_form").validate({
  ignore: "",
  rules: {
    date: {
      required: true,
    },
    submitted_by_agent: {
      required: true,
    },
    reference_number: {
      alphanum_special: true,
      required: true,
      maxlength: 15,
    },
    screening: {
      alphanum_special: true,
      required: true,
    },
    is_new_deal: {
      alphanum_special: true,
      required: true,
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

    unit_details: {
      alphanum_special: true,
      required: true,
      maxlength: 15,
    },

    building_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },

    rental_price: {
      numeric: false,
      required: false,
      maxlength: 100,
    },

    deal_start_date: {
      required: true,
    },

    deal_end_date: {
      required: true,
    },
    owner_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    owner_source: {
      required: true,
    },
    owner_mobile: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },
    mediating_agent_phone: {
      phoneNumber: true,
      minlength: 6,
      maxlength: 15,
    },
    owner_email: {
      custom_email: true,
      required: true,
      maxlength: 100,
    },
    tenant_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_source: {
      required: true,
    },
    tenant_mobile: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },
    tenant_email: {
      custom_email: true,
      required: true,
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
    agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    tenant_agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    mediating_agent_email: {
      custom_email: true,
      maxlength: 100,
    },
    owner_agency: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    agent_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    brn: {
      alphanum_special: true,
      maxlength: 255,
    },
    agent_phone: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },

    tenant_agency: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_agent_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_brn: {
      alphanum_special: true,

      maxlength: 255,
    },
    tenant_agent_phone: {
      phoneNumber: true,
      minlength: 6,
      maxlength: 15,
    },
    total_commission: {
      numeric: true,
      required: true,
      maxlength: 10,
    },
    less_outsude_commission: {
      alphanum_special: true,
      required: true,
      maxlength: 100,
    },
    net_commission: {
      numeric: true,
      required: true,
      maxlength: 10,
    },
    agent1: {
      required: true,
      numeric: true,
      maxlength: 10,
    },
    agent2: {
      numeric: true,
      maxlength: 10,
    },
    agent3: {
      numeric: true,
      maxlength: 10,
    },
    classic: {
      numeric: true,
      maxlength: 10,
    },

    plot_no: {
      alphanum_special: true,
      maxlength: 255,
    },

    mode_of_payment: {
      only_text: true,
      maxlength: 255,
    },
    agent_comment: {
      maxlength: 255,
    },

    comments: {
      maxlength: 255,
    },
    receipt_no: {
      alphanum_special: true,
      required: true,
      maxlength: 100,
    },
    is_rental_aml: {
      required: false,
    },

    kyc_number: {
      numeric: true,
      maxlength: 45,
    },
    property_size: {
      alphanum_special: true,
      maxlength: 255,
    },
    premises_no: {
      alphanum_special: true,
      maxlength: 255,
    },
    security_deposit: {
      numeric: false,
      maxlength: 255,
    },
    property_type: {
      required: false,
      alphanum_special: true,
      maxlength: 255,
    },
  },
  messages: {
    owner_mobile: {
      phoneNumber: "Phone number must only contain numbers and +",
    },
    mediating_agent_phone: {
      phoneNumber: "Phone number must only contain numbers and +",
    },
    tenant_mobile: {
      phoneNumber: "Phone number must only contain numbers and +",
    },
    agent_phone: {
      phoneNumber: "Phone number must only contain numbers and +",
    },
    tenant_agent_phone: {
      phoneNumber: "Phone number must only contain numbers and +",
    },
  },
  errorPlacement: function (error, element) {
    if (element.attr("type") == "radio") {
      var id = element.attr("id");
      $("#" + id + "_error").css("margin-right", "200px");
      error.addClass("field_error");
      error.insertAfter("#" + id + "_error");
    } else {
      k = error.insertAfter(element);
      console.log("Error placed after:", k);

    }
  },
});



$(document).on("click", "#create_deal", function (event) {
  console.log("clcike cthe button")
  $(
    '[name="submitted_by_agent"],[name="owner_agency"],[name="agent_first_name"],[name="agent_phone"],[name="tenant_agency"],[name="tenant_agent_first_name"],[name="tenant_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="receipt_no"],[name="is_sale_aml"],[name="agent_name1"],[name="is_rental_aml"]'
  ).each(function () {
    $(this).rules("add", "required");
  });
  if ($("#deal_form").valid()) {
    $("#save_as").val("update-deal");
    var url = "list/";

    if (
      countMultipleFiles("tenancy_contract") &
      countMultipleFiles("title_deed") &
      countMultipleFiles("owner_passport_copy") &
      countMultipleFiles("tenant_passport_visa_copy") &
      countMultipleFiles("rental_deposit_cheque_copy") &
      countMultipleFiles("tenancy_application_form") &
      countMultipleFiles("screening") &
      countMultipleFiles("key_hand_over_form") &
      checkKyc()
    ) {
      updatefunctionality(url);
    }
  } else {
    $("html, body").animate(
      {
        scrollTop: $(".main-header").offset(),
      },
      1000
    );
    var validator = $("#deal_form").validate();
          showErrors(validator);
    
  }
});



$(document).on('click', '#update_draft', function(event) {    
            $('[name="seller_agency"],[name="seller_agent_name"],[name="seller_agent_phone"],[name="buyer_agency"],[name="buyer_agent_name"],[name="buyer_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="agent_name1"],[name="receipt_no"],[name="is_sale_aml"]').each(function () {
                  $(this).rules('remove','required');
              });      
              if($('#deal_form').valid() & countMultipleFiles('screening')){  
                var url="draft/";   
                $('#save_as').val("update-draft");                         
                updatefunctionality(url);
               }else{
               $('html, body').animate({
                     scrollTop: $('.main-header').offset().top
                   }, 1000);
            }
              
           });







// count noof files in each file input field
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
    $(".nav-documents").closest(".form-group").find("span.text-danger").show();
  }
  return result;
}


function checkKyc() {
  var result = true;
  $("#rental_kyc_number_error").empty();
  $("#kyc_number_error").empty();
  var existing_count = parseInt($("#rental_kyc_number_existing_count").val());
  var removed_count = parseInt($("#rental_kyc_number_new_removed_count").val());
  if ($("#rental_kyc_number_new_removed_count").val() == "") {
    var removed_count = 0;
  }
  if (existing_count < 1 && removed_count < 1 && $("#kyc_number").val() == "") {
    result = false;
    $("#rental_kyc_number_error")
      .html("Either KYC Form or KYC Number is required!")
      .show();
    $("#kyc_number_error")
      .html("Either KYC Form or KYC Number is required!")
      .show();
    $(document).on("keyup", "input[name='kyc_number']", function (e) {
      $("#" + "kyc_number" + "_error").hide();
    });
  }
  return result;
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


function ValidateSizeadd(file,id,i){
	
    if(!/(\.jpg|\.jpeg|\.png|\.pdf)$/i.test(file.value))
    { 
      alert("Invalid image /pdf file type.");      
        $('#'+id).val('');  
        
        return false;   
    }   
      var FileSize = file.files[0].size;
      
      if (FileSize > 3000000)
      {
        $("#"+id+'_error').html('File size should be less than 3 MB').show();
        $('#'+id).val('');  
        return false;
      }else{
        $("#"+id+'_error').hide();
      }
  }