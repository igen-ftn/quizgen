
function previewSurvey() {

        $('#previewSurveyDiv').empty();
        questionNum = $("#questionSurveyDiv").children().length;

        var grammar ="<br/><p>Start test</p>"
         + "<p>" + "&nbsp;".repeat(4) + "\"" + $('#titleSurvey').val() + "\"" +"</p>"
         + "<p>" + "&nbsp;".repeat(4) + "Start survey" +"</p>";

         for (i = 1; i <= questionNum; i++) {
             var answerNum = $("#answersSurveyDiv" + i).children().length;
             grammar += "<p>" + "&nbsp;".repeat(8) + $('#questionSurvey' + i).val() +"</p>";
             if ($("#q" + i + 'type').val() === 'Open Ended'){
                grammar += "<p>" + "&nbsp;".repeat(16) + "Open ended</p>";
                grammar += "<p>" + "&nbsp;".repeat(16) + $("#q" + i + "presentation").val() + "</p>";
                continue;
             }
             else if($("#q" + i + 'type').val() === 'Multiple Choice'){
                grammar += "<p>" + "&nbsp;".repeat(16) + "multiple choice</p>";
                if ($("#q" + i + "multiple").val() === 'one answer'){
                    grammar += "<p>" + "&nbsp;".repeat(16) + "one answer</p>";
                }
                else{
                    grammar += "<p>" + "&nbsp;".repeat(16) + "multiple answers</p>";
                }
                for (j = 1; j <= answerNum; j++) {
                    var answer = $('#q' + i + 'SurveyAnswer' + j).val();
                    grammar += "<p>" + "&nbsp;".repeat(16) + answer + "</p>";
                }
                continue;
             }
             else if($("#q" + i + 'type').val() === 'Likert'){
                 grammar += "<p>" + "&nbsp;".repeat(16) + "Likert</p>";
                 for (j = 1; j <= answerNum; j++) {
                    var answer = $('#q' + i + 'SurveyAnswer' + j).val();
                    grammar += "<p>" + "&nbsp;".repeat(16) + answer + "</p>";
                 }
                 var statementNum = $("#statementDiv" + i).children().length;
                 for (j = 1; j <= statementNum; j++) {
                    var statement = $('#q' + i + 'statement' + j).val();
                    grammar += "<p>" + "&nbsp;".repeat(16) + statement + "</p>";
                 }
                 grammar += "<p>" + "&nbsp;".repeat(16) + $("#q" + i + "presentation").val() + "</p>";
                 continue;
             }
             else if($("#q" + i + 'type').val() === 'Semantic Diff'){
                 grammar += "<p>" + "&nbsp;".repeat(16) + "Semantic dif</p>";
                 for (j = 1; j <= answerNum; j++) {
                    var answer = $('#q' + i + 'SurveyAnswer' + j).val();
                    grammar += "<p>" + "&nbsp;".repeat(16) + answer + " " + $('#q' + i + 'semantic' + j).val() + "</p>";
                 }
                 grammar += "<p>" + "&nbsp;".repeat(16) + $("#q" + i + "presentation").val() + "</p>";
                 continue;
             }
             else if($("#q" + i + 'type').val() === 'Rank Order'){
                 grammar += "<p>" + "&nbsp;".repeat(16) + "Rank order</p>";
                 for (j = 1; j <= answerNum; j++) {
                    var answer = $('#q' + i + 'SurveyAnswer' + j).val();
                    grammar += "<p>" + "&nbsp;".repeat(16) + answer + "</p>";
                 }
                 continue;
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

        document.getElementById("q" + questionNum + 'type').disabled = true;

        if ($("#q" + questionNum + 'type').val() === 'Open Ended'){

            if (!document.getElementById("q" + questionNum + "presentation")){
                var presentation = "<select id=\"q" + questionNum + "presentation\" class=\"form-control\" style=\"width:30%;margin-left:43px;\">" +
                                "<option value=\"text area\">Text Area</option>" +
                                "<option value=\"input\">Text Input</option>" +
                            "</select>";
                $("#q" + questionNum + "select").append(presentation);
            }
            return;
        }

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
                                "<option value=\"multiple answers\">Multiple Answers</option>" +
                                "<option value=\"one answer\">One Answer</option>" +
                            "</select>";
                $("#q" + questionNum + "select").append(multiple);
            }
            return;
        }
        else if ($("#q" + questionNum + 'type').val() === 'Semantic Diff'){

            var semantic = "<div style=\"display: inline-block;margin-left:43px;\">" +
                                "<input id=\"q" + questionNum + "semantic" + answerNum + "\" type=\"number\" class=\"form-control\" style=\"width: 80px;\">" +
                            "</div>";

            if (!document.getElementById("q" + questionNum + "presentation")){
                var presentation = "<select id=\"q" + questionNum + "presentation\" class=\"form-control\" style=\"width:30%;margin-left:43px;\">" +
                                "<option value=\"slider\">Slider</option>" +
                                "<option value=\"radio group\">Radio Group</option>" +
                            "</select>";
                $("#q" + questionNum + "select").append(presentation);
            }

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
                                "<option value=\"slider\">Slider</option>" +
                                "<option value=\"radio group\">Radio Group</option>" +
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

function getCookie(name) {
    var cookieValue = null;
    if(document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function submitSurvey() {

        previewSurvey();
        var node = document.getElementById('previewSurveyDiv')
        var url = '/new_survey/';
        var csrftoken = getCookie('csrftoken')
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            type: "POST",
            url: url,
            data: {
              'content': node.textContent.replace(/\s\s+/g, ' '),
              'title' : $('#titleSurvey').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.status)
                    window.location.href = '/survey/';
                else
                    alert(data.message)
            },
            error: function (data) {
                alert("Error")
            }
        });

}


