// To toggle visibility of next or previous pages when adding a new employee
// var visibleDiv = 0;
// function showDiv()
// {
//   $(".pager").hide();
//   $(".pager:eq("+ visibleDiv +")").show();
// }
// showDiv()

// function next()
// {
// if(visibleDiv== $(".pager").length-1)
// {
//   visibleDiv = 0;
// }
// else {
//   visibleDiv ++;
// }
// showDiv();
// }


// function prev()
// {
// if (visibleDiv == 0)
// {
//   visibleDiv= $(".pager").length-1
// }
// else {
//   visibleDiv --;
// }
// showDiv();
// }

//To Upload Profile Picture
function previewImage(event) {
  var input = event.target;
  var reader = new FileReader(); //reads the selected file using the FileReader API
  reader.onload = function() {
      var img = document.getElementById('preview-image');
      img.src = reader.result; /** sets the src attribute of the preview image (<img>) to the data URL of the selected image.
                                   This allows the image to be displayed as a preview before submitting the form. **/
  }
  reader.readAsDataURL(input.files[0]);
}