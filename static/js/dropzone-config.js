Dropzone.autoDiscover = false;

document.addEventListener('DOMContentLoaded', function () {
  const myDropzone = new Dropzone("#my-dropzone", {
    url: "/file-process",
    uploadMultiple: true,
    parallelUploads: 100,
    paramName: "file",

    init: function() {
      var dropzone = this;

      this.on("successmultiple", function(files, response) {
        console.log("Success multiple:", response);

        files.forEach(file => {
          dropzone.removeFile(file);
        });

        updateFileList();
      });

      this.on("success", function(file, response) {
        console.log("Success single:", response);
        dropzone.removeFile(file);
        updateFileList();
      });

      this.on("error", function(file, errorMessage, xhr) {
        console.error("Upload error:", errorMessage);
      });
    }
  });

  updateFileList();
});

function updateFileList() {
    fetch('/get_files')
        .then(response => response.json())
        .then(files => {
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = '<h3>Processed Files:</h3>';

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
                        <span class="file-size">(${file.size}KB)</span>
                        <button class="delete-btn">X</button>
                    </div>
                `;
                const deleteBtn = fileDiv.querySelector('.delete-btn');
                deleteBtn.addEventListener('click', () => {
                  // Send request to server to delete file
                  fetch(`/delete_file?name=${encodeURIComponent(file.name)}`, {
                      method: 'DELETE'
                  })
                  .then(response => {
                      if (!response.ok) {
                          throw new Error("Failed to delete file");
                      }
                      return response.json();
                  })
                  .then(result => {
                      if (result.success) {
                          // Remove from DOM only if deletion was successful
                          fileList.removeChild(fileDiv);
                      } else {
                          alert("Failed to delete the file.");
                      }
                  })
                  .catch(error => {
                      console.error("Error deleting file:", error);
                      alert("Error deleting file.");
                  });
              });

                fileList.appendChild(fileDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching files:', error);
            document.getElementById('file-list').innerHTML = '<p>Error loading files.</p>';
        });
}
