let fileList = [];

// Create main request
const request = new XMLHttpRequest();

// Form list
const formList = document.getElementById("form-list");

// Create more file button li
const moreButtonLi = document.createElement("li");
// Form submit button
const submitTransfer = document.getElementById("submit-transfer");

// Uploaded files UL
const uploadedFileList = document.getElementById("uploaded-file-list");

// Get hidden inputs
const hiddenFileInput = document.getElementById("hidden-file-input");

// Get card body
const cardBody = document.getElementById("card-body");

// Get card Footer
const cardFooter = document.querySelector(".card-footer");

// Handle file input click
const handleFileInputClick = () => {
  hiddenFileInput.click();
};

// Add event listeners to buttons
document
  .getElementById("upload-file-button")
  .addEventListener("click", handleFileInputClick);
document
  .getElementById("upload-file-text")
  .addEventListener("click", handleFileInputClick);

const convertSize = (bytes) => {
  const kb = bytes * 0.001;
  if (kb === 0) {
    return `${bytes} bytes`;
  }
  const truncate = Math.trunc(kb);
  return `${truncate} KB`;
};

// For each file in file list append li
const handleAddFileLiToList = () => {
  fileList.forEach((file, index) => {
    // Create Li
    const li = document.createElement("li");
    li.className =
      "file-list-item list-group-item d-flex justify-content-between align-items-start bg-light";
    const liHtml = `
      <div class="ms-2 me-auto">
        <div style="max-width:200px; line-height:1.1;" class="my-0 text-wrap">${
          file.name
        }</div>
        <div class="file-info text-muted fw-light my-0">${convertSize(
          file.size
        )} - ${file.type}</div>
      </div>
    `;
    li.innerHTML = liHtml;

    // Create Delete button
    const deleteButton = document.createElement("span");
    deleteButton.className =
      "file-delete-button badge hover bg-danger rounded-pill";
    deleteButton.innerHTML = "x";
    deleteButton.addEventListener("click", () => {
      handleItemDelete(index);
    });

    // Append Li
    uploadedFileList.appendChild(li);

    // Append delete button
    li.appendChild(deleteButton);
  });
};

const handleItemDelete = (index) => {
  fileList.splice(index, 1);
  updateFileListHtml();
};

// Hide main card body
const handleUploadButtonVisibilityToggle = () => {
  if (fileList.length <= 0) {
    cardBody.classList.remove("visually-hidden");
  } else {
    cardBody.classList.add("visually-hidden");
  }
};

// Append add more button to UL
const handleMoreButtonLiAppend = () => {
  const moreButtonLiHtml = `
    <div class="d-flex align-items-center">
      <div class="upload-icon text-primary">
        <div>
          <i class="fas fa-plus-circle fa-2x"></i>
        </div>
      </div>
      <div class="d-flex justify-content-center text-muted flex-column mx-2">
        <span class="d-block">Add more files</span>
        <div class="remaining-space">
          <span class="fw-light">1 file added - </span>
          <span class="fw-light">2.0 GB remaining</span>
        </div>
      </div>
    </div>
  `;

  // If files in list append Li
  if (fileList.length > 0) {
    // Add ID and classes to li
    moreButtonLi.id = "upload-more-button";
    moreButtonLi.className = "hover list-group-item py-3 bg-light";

    // Set li inner html and append to list
    moreButtonLi.innerHTML = moreButtonLiHtml;
    uploadedFileList.appendChild(moreButtonLi);

    // Add event listener to button
    moreButtonLi.addEventListener("click", handleFileInputClick);

    // Remove if no files
  } else {
    moreButtonLi.removeEventListener("click", handleFileInputClick);
    moreButtonLi.remove();
  }
};

// File upload input change handler
const handleUploadFile = (e) => {
  // Add file to list
  fileList.push(e.target.files[0]);
  e.target.value = "";
  updateFileListHtml();
};

const updateFileListHtml = () => {
  // Rest file list Ul
  uploadedFileList.innerHTML = "";
  handleAddFileLiToList();

  handleUploadButtonVisibilityToggle();
  handleMoreButtonLiAppend();
};

hiddenFileInput.addEventListener("change", handleUploadFile, false);

const handleCardReset = () => {
  window.location.reload();
};

const handleResponse = (response) => {
  const url = response.url;
  // Set card body empty html
  const cardProgressHtml = `
            <div class="completed-container text-center">
                <h3>Upload complete</h3>
                <p class="py=0">Your URL is:</p>
                <a target="blank" href=${url} class="underline">${url}</a>
            </div>
        `;
  cardBody.innerHTML = cardProgressHtml;

  // Create reset button
  const resetButton = document.createElement("button");
  resetButton.onclick = handleCardReset;
  resetButton.className = "w-100 btn btn-lg btn-primary";
  resetButton.innerHTML = "New Transfer";

  // Show card footer and add reset button
  cardFooter.classList.remove("visually-hidden");
  cardFooter.innerHTML = "";
  cardFooter.appendChild(resetButton);
};

const updatePercentage = (percentage) => {
  if (document.body.contains(formList)) {
    formList.classList.add("visually-hidden");
  }
  // Remove file list and form list
  uploadedFileList.remove();
  handleUploadButtonVisibilityToggle();
  cardFooter.classList.add("visually-hidden");

  // Set card body empty html
  const cardProgressHtml = `
    <div class="progress-container text-center">
      <div class="progress">
        <div class="progress-bar progress-bar-striped progress-bar-animated" 
        role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: ${percentage}%"></div>
      </div>    
      <p class="py-5">Progress: ${percentage} %</p>
    </div>
  `;
  cardBody.innerHTML = cardProgressHtml;
};

request.upload.addEventListener("progress", (e) => {
  if (e.lengthComputable) {
    const percentage = Math.round((e.loaded * 100) / e.total);
    updatePercentage(percentage);
  }
});

request.addEventListener("load", (e) => {
  if (request.readyState === 4 && request.status === 200) {
    handleResponse(JSON.parse(request.response));
  }
});

const checkInputValid = (input, formIsValid) => {
  if (input.value === "") {
    input.classList.add("is-invalid");
    formIsValid = false;
  } else {
    input.classList.remove("is-invalid");
  }
  return formIsValid;
};

const handleSubmitData = (e) => {
  let formIsValid = true;
  const uri = "/upload-files";
  const data = new FormData();
  const fromEmail = document.getElementById("from-email-input");
  const toEmail = document.getElementById("to-email-input");
  const message = document.getElementById("message-input");

  // Check at least one file uploaded
  if (fileList.length === 0) {
    hiddenFileInput.classList.add("is-invalid");
    formIsValid = false;
  } else {
    hiddenFileInput.classList.remove("is-invalid");
  }

  // Check inputs are valid
  const inputs = [fromEmail, toEmail];
  inputs.forEach((input) => {
    formIsValid = checkInputValid(input, formIsValid);
  });

  // If form is not valid return
  if (!formIsValid) {
    return;
  }

  // Open request if all forms are valid
  request.open("POST", uri, true);

  // Build form data
  for (const file of fileList) {
    data.append("files[]", file, file.name);
  }
  data.append("to_email", toEmail.value);
  data.append("from_email", fromEmail.value);
  data.append("message", message.value);

  // Empty file list
  fileList = [];

  request.send(data);
};

// Update uploaded file list on input change
submitTransfer.addEventListener("click", handleSubmitData);