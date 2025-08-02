Dropzone.autoDiscover = false;

document.addEventListener('DOMContentLoaded', function () {
  const myDropzone = new Dropzone("#my-dropzone", {
    url: "/file-process",
    uploadMultiple: true,
    parallelUploads: 100,
    paramName: "file",
    addRemoveLinks: true,
    // autoProcessQueue is true by default, no need to set it
  });

  // Optional: Add uploaded files to the list
//  myDropzone.on("successmultiple", function (files, response) {
//    const list = document.getElementById("file-list");
//    files.forEach(file => {
//      const item = document.createElement("li");
//      item.textContent = file.name;
//      list.appendChild(item);
//    });
//  });
});
