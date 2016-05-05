$(document).ready(function(){
    var input = document.getElementById('tr_search');
    new Awesomplete(input, {
        list: [],
        data: function(text, input){
            alert(text);
            return {1:1,2:2,3:3}
            }
        });
    });

