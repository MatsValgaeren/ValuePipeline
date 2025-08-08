Dropzone.autoDiscover = false;

document.addEventListener('DOMContentLoaded', function () {
  const myDropzone = new Dropzone("#my-dropzone", {
    url: "/file-process",
    uploadMultiple: true,
    parallelUploads: 100,
    paramName: "file",

//    init: function() {
//      this.on("successmultiple", function(files, response) {
//        // Remove files immediately
//        files.forEach(file => {
//          this.removeFile(file);
//        });
//        updateFileList();
//      });
//
//      this.on("success", function(file, response) {
//        this.removeFile(file);
//        updateFileList();
//      });
//    }
//  });
});

  // Update file list when dropzone completes upload
  myDropzone.on("successmultiple", function (files, response) {
    // Wait a bit for server processing, then update
    setTimeout(updateFileList, 1000);
  });

  myDropzone.on("success", function (file, response) {
    // Also handle single file uploads
    setTimeout(updateFileList, 1000);
  });

  // Load initial file list
  updateFileList();
});

function updateFileList() {
    fetch('/get_files')
        .then(response => response.json())
        .then(files => {
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = '<h3>Current Files:</h3>';

            if (files.length === 0) {
                fileList.innerHTML += '<p>No files uploaded yet.</p>';
                return;
            }

            files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'file-item';
                fileDiv.innerHTML = `
                    <div class="file-info">
                        📁 ${file.name}
                        <span class="file-size">(${file.size})</span>
                    </div>
                `;
                fileList.appendChild(fileDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching files:', error);
            document.getElementById('file-list').innerHTML = '<p>Error loading files.</p>';
        });
}

// Initialize socket connection
const socket = io();

// Listen for file upload events from other users
socket.on('file_uploaded', function(data) {
    console.log('File uploaded:', data.filename);
    updateFileList(); // Refresh file list when any user uploads
});