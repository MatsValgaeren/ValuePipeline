Dropzone.autoDiscover = false;

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  const myDropzone = new Dropzone("#my-dropzone", {
    url: "/file-process",
    uploadMultiple: true,
    autoProcessQueue: false,
    parallelUploads: 100,
    paramName: "file",
    addRemoveLinks: true
  });

  document.getElementById("process-btn").addEventListener("click", function() {
    myDropzone.processQueue();
  });


  const fileList = document.getElementById('file-list');


    myDropzone.on("addedfile", function(file) {
      const li = document.createElement('li');
      li.id = `file-list-item-${file.upload.uuid || file.name}`;
      li.textContent = file.name;
      fileList.appendChild(li);
    });

    myDropzone.on("successmultiple", function(files, response) {
      files.forEach(function(file) {
        myDropzone.removeFile(file);

        let li = document.getElementById(`file-list-item-${file.upload.uuid || file.name}`);
        if (li) {
          li.textContent += ' - Processed';
        }
      });
    });
});