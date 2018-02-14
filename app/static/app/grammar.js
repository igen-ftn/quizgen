var answerNum = 3;
var questionNum = 1;

function previewQuiz() {

        $('#previewDiv').empty();

        var grammar ="<br/><p>Start test</p>"
         + "<p>" + "&nbsp;".repeat(4) + "\"" + $('#title').val() + "\"" +"</p>"
         + "<p>" + "&nbsp;".repeat(4) + "Start quiz" +"</p>"
         + "<p>" + "&nbsp;".repeat(8) + $('#question1').val() +"</p>";
         for (i = 1; i < answerNum; i++) {
            var answer = $('#q' + questionNum + 'answer' + i).val();
            grammar += "<p>" + "&nbsp;".repeat(16) + answer;
            if (document.getElementById("q" + questionNum + "ans" + i).checked){
                grammar += " +";
            }
            else{
                grammar += " -";
            }
            grammar += "</p>";
        }
         grammar += "<p>" + "&nbsp;".repeat(4) + "End quiz" +"</p>"
         + "<p>End test</p>";

        $('#previewDiv').append(grammar);

        $('#previewDiv').css("border", "1px solid #ccc")
        $('#previewDiv').css("border-radius", "4px")

}

function addAnswer(questionNum) {

        var newAnswer = "<div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                    "<div class=\"col-sm-8 form-inline\">" +
                      "<input type=\"text\" id=\"q" + questionNum + "answer" + answerNum +"\" class=\"form-control\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                        "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                            "<input id=\"q" + questionNum + "ans" + answerNum + "\" type=\"checkbox\">" +
                            "<label for=\"q" + questionNum + "ans" + answerNum + "\">" +
                            "</label>" +
                        "</div>" +
                    "</div>" +
                "</div>"

        $('#answersDiv' + questionNum).append(newAnswer);
        answerNum++;

}

function addQuestion() {

        questionNum++;
        answerNum = 3;

        var newQuestion = "<div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Question:</label>" +
                    "<div class=\"col-sm-8\">" +
                        "<textarea  class=\"form-control\" id=\"question" + questionNum + "\" rows=\"5\" style=\"width:88%; resize:none;\">Question &lt;order&gt; &lt;\" + text + \"&gt; &lt;'one answer'/'multiple answers'&gt;</textarea>" +
                    "</div>" +
                "</div>" +
                "<div class=\"form-group\">" +
                    "<div class=\"col-sm-8\">" +
                        "<label class=\"control-label\" style=\"float:right;\">Correct Answer</label>" +
                    "</div>" +
                "</div>" +
                "<div id=\"answersDiv" + questionNum + "\">" +
                    "<div class=\"form-group\">" +
                        "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                        "<div class=\"col-sm-8 form-inline\">" +
                          "<input type=\"text\" class=\"form-control\" id=\"q" + questionNum + "answer" + answerNum + "\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                            "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "ans" + answerNum + "\" type=\"checkbox\">" +
                                "<label for=\"q" + questionNum + "ans" + answerNum + "\">" +
                                "</label>" +
                            "</div>" +
                        "</div>" +
                        "<div>" +
                            "<button type=\"button\" class=\"btn btn-success btn-circle\" onclick=\"addAnswer(" + questionNum + ")\"><span class=\"glyphicon glyphicon-plus-sign\"></span>  Add Answer</button>" +
                        "</div>" +
                    "</div>" +
                    "<div class=\"form-group\">" +
                        "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                        "<div class=\"col-sm-8 form-inline\">" +
                            "<input type=\"text\"  class=\"form-control\" id=\"q1answer" + questionNum + "\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                            "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "ans" + answerNum + "\" type=\"checkbox\">" +
                                "<label for=\"q" + questionNum + "ans" + answerNum + "\">" +
                                "</label>" +
                            "</div>" +
                        "</div>" +
                    "</div>" +
                "</div><br/>";

        $('#questionDiv').append(newQuestion);
        answerNum++;

}