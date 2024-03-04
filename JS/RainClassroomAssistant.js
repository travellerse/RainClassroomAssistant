// ==UserScript==
// @name         RainClassroomAssistant
// @namespace    https://github.com/travellerse/RainClassroomAssitant
// @version      0.0.1
// @description  try to take over the world!
// @author       You
// @match        https://pro.yuketang.cn/v2/web/quizSummary/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.com
// @grant        none
// ==/UserScript==

(function () {
    'use strict';
    const quizUrl = 'https://pro.yuketang.cn/v2/api/web/quiz/personal_result?';
    if (window.location.href.indexOf('https://pro.yuketang.cn/v2/web/quizSummary/') != -1) {
        var classroom_id = window.location.href.split('/')[6];
        var quiz_id = window.location.href.split('/')[7];
        console.log(classroom_id, quiz_id);

        var results = getResult(classroom_id, quiz_id);


    }


    /*{
"errcode": 0,
"errmsg": "Success",
"data": {
"answer_time": null,
"objective_result_list": [
    {
        "problem_index": 1,
        "class_average": 0.94,
        "problem_id": 15583730,
        "score": 2,
        "result": "C",
        "answer": "C",
        "problem_type": 1,
        "correct": true
    },
    {
        "problem_index": 2,
        "class_average": 0.96,
        "problem_id": 15583731,
        "score": 2,
        "result": "B",
        "answer": "B",
        "problem_type": 1,
        "correct": true
    },
    {
        "problem_index": 3,
        "class_average": 0.74,
        "problem_id": 15583732,
        "score": 0,
        "result": "B",
        "answer": "A",
        "problem_type": 1,
        "correct": false
    },
    {
        "problem_index": 4,
        "class_average": 1,
        "problem_id": 15583733,
        "score": 2,
        "result": "A",
        "answer": "A",
        "problem_type": 1,
        "correct": true
    },
    {
        "problem_index": 5,
        "class_average": 0.89,
        "problem_id": 15583734,
        "score": 0,
        "result": "B",
        "answer": "A",
        "problem_type": 1,
        "correct": false
    },
    {
        "problem_index": 6,
        "class_average": 0.96,
        "problem_id": 15583735,
        "score": 2,
        "result": "C",
        "answer": "C",
        "problem_type": 1,
        "correct": true
    },
    {
        "problem_index": 7,
        "class_average": 0.96,
        "problem_id": 15583736,
        "score": 5,
        "result": "F",
        "answer": "F",
        "problem_type": 1,
        "correct": true
    }
],
"score": 13,
"title": "第一章第一节  测试(4)",
"unfinished_count": 0,
"problem_count": 7,
"quiz_visible": true,
"publish_time": 1709019673000,
"deadline": 1709827140000,
"incorrect_count": 2,
"duration": 213491,
"limit": 0,
"subjective_result_list": [],
"full_score": 17,
"objective_score": 13
}
}
*/
    function getResult(classroom_id, quiz_id) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', quizUrl + 'classroom_id=' + classroom_id + '&quiz_id=' + quiz_id, true);
        xhr.send();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var res = JSON.parse(xhr.responseText);
                console.log(res);
                if (res.errcode == 0) {
                    results = res.data.objective_result_list;
                    console.log(results);
                }
            }
        }
        return results;
    }

    // Your code here...
})();