
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
                if (document.getElementById("q" + i + "SurveyAns" + j).checked){              // proveriti samo za multiple choice
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

        if ($("#q" + questionNum + 'type').val() === 'Open Ended'){
            return;
        }

        document.getElementById("q" + questionNum + 'type').disabled = true;

        var newAnswer = "<div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Answer:</label>" +
                    "<div class=\"col-sm-8 form-inline\" id=\"q" + questionNum + "div" + answerNum +"\">" +
                      "<input type=\"text\" id=\"q" + questionNum + "SurveyAnswer" + answerNum +"\" class=\"form-control\" style=\"width:70%\" placeholder=\"Answer <&quot + tag + &quot> <&quot + text + &quot>\">" +
                    "</div>" +
                "</div>";

        $('#answersSurveyDiv' + questionNum).append(newAnswer);

        if ($("#q" + questionNum + 'type').val() === 'Multiple Choice'){

            if (!document.getElementById("q" + questionNum + "multiple")){
                var multiple = "<select id=\"q" + questionNum + "multiple\" class=\"form-control\" style=\"width:30%;margin-left:43px;\">" +
                                "<option>Multiple Answers</option>" +
                                "<option>One Answer</option>" +
                            "</select>";
                $("#q" + questionNum + "select").append(multiple);
            }
            return;
        }
        else if ($("#q" + questionNum + 'type').val() === 'Semantic Diff'){

            var semantic = "<div style=\"display: inline-block;margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "semantic" + answerNum + "\" type=\"number\" class=\"form-control\" style=\"width: 80px;\">" +
                            "</div>";

            document.getElementById('q' + questionNum + "SurveyAnswer" + answerNum).placeholder="Answer <'left'>/<'right'> <\" + text + \">";
            $('#q' + questionNum + "div" + answerNum).append(semantic);
            return;
        }
        else if ($("#q" + questionNum + 'type').val() === 'Rank Order'){

            document.getElementById('q' + questionNum + "SurveyAnswer" + answerNum).placeholder="Answer <\" + text + \">";
            return;
        }
        else if ($("#q" + questionNum + 'type').val() === 'Likert'){

            if (!document.getElementById("q" + questionNum + "presentation")){
                var presentation = "<select id=\"q" + questionNum + "presentation\" class=\"form-control\" style=\"width:30%;margin-left:43px;\">" +
                                "<option>Slider</option>" +
                                "<option>Radio Group</option>" +
                            "</select>";
                $("#q" + questionNum + "select").append(presentation);
            }

            if (!document.getElementById("statementButton" + questionNum)){
                var button = "<br/><div>" +
                                "<button type=\"button\" class=\"btn btn-success btn-circle\" id=\"statementButton" + questionNum + "\" style=\"float:right;margin-right:160px;\"" +
                                "onclick=\"addStatement(" + questionNum + ")\"><span class=\"glyphicon glyphicon-plus-sign\"></span>  Add Statement</button>" +
                            "</div>";
                $("#q" + questionNum + "buttons").append(button);
            }

            document.getElementById('q' + questionNum + "SurveyAnswer" + answerNum).placeholder="Answer <order> <\" + text + \">";
            return;
        }

}

function addStatement(questionNum) {

        var statementNum = $("#statementDiv" + questionNum).children().length + 1;

        var newStatement = "<div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Statement:</label>" +
                    "<div class=\"col-sm-8\">" +
                      "<input type=\"text\" id=\"q" + questionNum + "statement" + statementNum +"\" class=\"form-control\" style=\"width:70%\" placeholder=\"Statement <&quot + text + &quot>\">" +
                    "</div>" +
                "</div>";

        $('#statementDiv' + questionNum).append(newStatement);
}

function addSurveyQuestion() {

        var questionNum = $("#questionSurveyDiv").children().length + 1;

        var newQuestion = "<div><div class=\"form-group\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Question:</label>" +
                    "<div class=\"col-sm-8\">" +
                        "<textarea  class=\"form-control\" id=\"questionSurvey" + questionNum + "\" rows=\"5\" style=\"width:88%; resize:none;\" placeholder=\"Question <order> <&quot + text + &quot>\"></textarea>" +
                    "</div>" +
                "</div>" +
                "<div class=\"form-group\" id=\"q" + questionNum + "buttons\">" +
                    "<label class=\"col-sm-2 control-label\" style=\"text-align:left; width:100px;\">Type:</label>" +
                    "<div class=\"col-sm-8 form-inline\" id=\"q" + questionNum + "select\">" +
                        "<select id=\"q" + questionNum + "type\" class=\"form-control\" style=\"width:30%;\">" +
                            "<option>Multiple Choice</option>" +
                            "<option>Likert</option>" +
                            "<option>Semantic Diff</option>" +
                            "<option>Rank Order</option>" +
                            "<option>Open Ended</option>" +
                        "</select>" +
                    "</div>" +
                    "<div>" +
                        "<button type=\"button\" class=\"btn btn-success btn-circle\" onclick=\"addSurveyAnswer(" + questionNum + ")\"><span class=\"glyphicon glyphicon-plus-sign\"></span>  Add Answer</button>" +
                    "</div>" +
                "</div>" +
                "<div id=\"answersSurveyDiv" + questionNum + "\">" +
                "</div>" +
                "<div id=\"statementDiv" + questionNum + "\">" +
                "</div>" +
                "<br/></div>";

        $('#questionSurveyDiv').append(newQuestion);

}

