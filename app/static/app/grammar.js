
function previewQuiz() {

        $('#previewDiv').empty();

        var grammar ="<br/><p>Start test</p>"
         + "<p>" + "&nbsp;".repeat(4) + "\"" + $('#title').val() + "\"" +"</p>"
         + "<p>" + "&nbsp;".repeat(4) + "Start quiz" +"</p>"
         + "<p>" + "&nbsp;".repeat(8) + $('#question1').val() +"</p>"

         + "<p>" + "&nbsp;".repeat(4) + "End quiz" +"</p>"
         + "<p>End test</p>";

        $('#previewDiv').append(grammar);

        $('#previewDiv').css("border", "1px solid #ccc")
        $('#previewDiv').css("border-radius", "4px")

}