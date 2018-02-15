
function previewSurvey() {

        $('#previewSurveyDiv').empty();
        questionNum = $("#questionSurveyDiv").children().length;

        var grammar ="<br/><p>Start test</p>"
         + "<p>" + "&nbsp;".repeat(4) + "\"" + $('#titleSurvey').val() + "\"" +"</p>"
         + "<p>" + "&nbsp;".repeat(4) + "Start survey" +"</p>";

         for (i = 1; i <= questionNum; i++) {
             var answerNum = $("#answersSurveyDiv" + i).children().length;
             grammar += "<p>" + "&nbsp;".repeat(8) + $('#questionSurvey' + i).val() +"</p>";
             for (j = 1; j <= answerNum; j++) {
                var answer = $('#q' + i + 'SurveyAnswer' + j).val();
                grammar += "<p>" + "&nbsp;".repeat(16) + answer;
                if (document.getElementById("q" + i + "SurveyAns" + j).checked){
                    grammar += " +";
                }
                else{
                    grammar += " -";
                }
                grammar += "</p>";
            }
         }
         grammar += "<p>" + "&nbsp;".repeat(8) + "button ok \"Submit\"" +"</p>"
         + "<p>" + "&nbsp;".repeat(4) + "End survey" +"</p>"
         + "<p>End test</p>";

        $('#previewSurveyDiv').append(grammar);

        $('#previewSurveyDiv').css("border", "1px solid #ccc")
        $('#previewSurveyDiv').css("border-radius", "4px")

}

function addSurveyAnswer(questionNum) {

        var answerNum = $("#answersSurveyDiv" + questionNum).children().length + 1;

        var newAnswer = "<div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                    "<div class=\"col-sm-8 form-inline\">" +
                      "<input type=\"text\" id=\"q" + questionNum + "SurveyAnswer" + answerNum +"\" class=\"form-control\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                        "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                            "<input id=\"q" + questionNum + "SurveyAns" + answerNum + "\" type=\"checkbox\">" +
                            "<label for=\"q" + questionNum + "SurveyAns" + answerNum + "\">" +
                            "</label>" +
                        "</div>" +
                    "</div>" +
                "</div>"

        $('#answersSurveyDiv' + questionNum).append(newAnswer);

}

function addSurveyQuestion() {

        var questionNum = $("#questionSurveyDiv").children().length + 1;

        var newQuestion = "<div><div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Question:</label>" +
                    "<div class=\"col-sm-8\">" +
                        "<textarea  class=\"form-control\" id=\"questionSurvey" + questionNum + "\" rows=\"5\" style=\"width:88%; resize:none;\">Question &lt;order&gt; &lt;\" + text + \"&gt; &lt;'one answer'/'multiple answers'&gt;</textarea>" +
                    "</div>" +
                "</div>" +
                "<div class=\"form-group\">" +
                    "<div class=\"col-sm-8\">" +
                        "<label class=\"control-label\" style=\"float:right;\">Correct Answer</label>" +
                    "</div>" +
                "</div>" +
                "<div id=\"answersSurveyDiv" + questionNum + "\">" +
                    "<div class=\"form-group\">" +
                        "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                        "<div class=\"col-sm-8 form-inline\">" +
                          "<input type=\"text\" class=\"form-control\" id=\"q" + questionNum + "SurveyAnswer1\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                            "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "SurveyAns1\" type=\"checkbox\">" +
                                "<label for=\"q" + questionNum + "SurveyAns1\">" +
                                "</label>" +
                            "</div>" +
                        "</div>" +
                        "<div>" +
                            "<button type=\"button\" class=\"btn btn-success btn-circle\" onclick=\"addSurveyAnswer(" + questionNum + ")\"><span class=\"glyphicon glyphicon-plus-sign\"></span>  Add Answer</button>" +
                        "</div>" +
                    "</div>" +
                    "<div class=\"form-group\">" +
                        "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                        "<div class=\"col-sm-8 form-inline\">" +
                            "<input type=\"text\"  class=\"form-control\" id=\"q" + questionNum + "SurveyAnswer2\" style=\"width:70%\" value=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                            "<div class=\"checkbox checkbox-circle\" style=\"margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "SurveyAns2\" type=\"checkbox\">" +
                                "<label for=\"q" + questionNum + "SurveyAns2\">" +
                                "</label>" +
                            "</div>" +
                        "</div>" +
                    "</div>" +
                "</div><br/></div>";

        $('#questionSurveyDiv').append(newQuestion);

}

