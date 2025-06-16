console.log("custom.js loaded");

let formInitialized = false;

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

$(document).ready(function () {
  if (!formInitialized) {
    console.log("Form not initialized, setting up.");
    // Initialize form elements here

    console.log("Document is ready!");

    // Handle form submission
    $("#filterForm").on("submit", function (e) {
      e.preventDefault();

      const formData2 = Object.fromEntries(
        new URLSearchParams($(this).serialize())
      ); // serialize form fields
      console.log("Form data:", formData2); // Log the serialized form data
      postAndRedirect("/api/rental-deals/filter/", formData2);
    });
    $("#filterForm").trigger("submit");
    formInitialized = true; // Set the flag to true after initialization
  }
});

function postAndRedirect(postUrl, formData1) {
  const formData = new FormData();

  const lastPart = window.location.pathname
    .split("/")
    .filter(Boolean)
    .slice(-1)[0];
  console.log(lastPart);

  for (const key in formData1) {
   
    if (lastPart === "all" && key === "type") {
      
      formData.append(key, "All");
      console.log(`Appending ${key}: all`,  );;
    }
    else if (lastPart === "draft" && key === "type") {
      formData.append(key, "draft");
      console.log(`Appending ${key}: draft`,  );;
    }  
    else if (lastPart === "approved" && key === "type") {
      formData.append(key, "approved");
      console.log(`Appending ${key}: approved`,  );;
    }  
    else if (lastPart === "pending" && key === "type") {
      formData.append(key, "pending");
      console.log(`Appending ${key}: pending`,  );;
    }  
    else if (lastPart === "waiting" && key === "type") {
      formData.append(key, "waiting");
      console.log(`Appending ${key}: waiting`,  );;
    }  
    else if (lastPart === "rejected" && key === "type") {
      formData.append(key, "rejected");
      console.log(`Appending ${key}: rejected`,  );;
    }  
    else if (lastPart === "entered-finance" && key === "type") {
      formData.append(key, "entered-finance");
      console.log(`Appending ${key}: entered-finance`,  );;
    }  

    else if (lastPart === "waiting-finance" && key === "type") {
      formData.append(key, "waiting-finance");
      console.log(`Appending ${key}: waiting-finance`,  );;
    }  
    

    else {
      formData.append(key, formData1[key]);
    }

     
  }

  console.log("Form data to be sent:", formData);

  fetch(postUrl, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
    credentials: "include",
  })
    .then((response) => {
      console.log("Response status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Response data:", data.data);
      const rentalDeals = data.data || data; // use data.data if your API wraps it

      $("#myTable").DataTable({
        data: rentalDeals, // ✅ Pass the array directly
        destroy: true, // ❗Needed if reinitializing table
        columns: [
          { data: "id", title: "ID" },
          { data: "reference_number", title: "Ref No" },
          { data: "agent_first_name", title: "Agent" },
          { data: "tenant_first_name", title: "Tenant" },
          { data: "building_name", title: "Building" },
          { data: "project_name", title: "Project" },
          { data: "rental_price", title: "Price" },
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
    .catch((error) => {
      console.error("POST error:", error);
    });
}
