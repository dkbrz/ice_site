// const config = require('config');
// const API_URL = config.get('API.API_URL');
// console.log(API_URL)


$(document).ready(

  function() {

    // Если нажали на кнопку выдвинуть информацию о команде проекта, схлопываем и меняем значок
    $(".btn-slide").click( function() {
      $("#team-list").slideToggle("show");
      $(this).toggleClass("active");

      if ($("#caret-sigh").hasClass("bi-caret-up")) {
        $("#caret-sigh").attr("class", "bi-caret-down");
        $("path", this).attr("d", 
          "M3.204 5L8 10.481 12.796 5H3.204zm-.753.659l4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z");
        console.log("caret-down");
      } else if ($("#caret-sigh").hasClass("bi-caret-down")) {
          $("#caret-sigh").attr("class", "bi-caret-up");
          $("path", this).attr("d", 
            "M3.204 11L8 5.519 12.796 11H3.204zm-.753-.659l4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z");
          console.log("caret-up");}
    });


     let condition1 = (/\/formula\//.test(this.location.pathname));
     let condition2 = ($( ".formula-example" ).length <= 0);
     let condition3 = (window.location.pathname == '/');

     // Если это страница контекста формулы и нет никаких данных, вставить предупреждалку с ошибкой
     if (condition1 && condition2) {
       insertEmptyOutputPlaque();
     }


     if (condition3) {
       preventPageReboot();
     } else {
       getFormItems();
     }


     // Если на старнице с выдачей контестов формул нажали на знак вернуться к началу страницы
     $(".caret-up-btn").click( function() {
       window.location.replace("#");
     });
  
  }
);



// Предотвращает перезагрузку страницы
function preventPageReboot(){
  $(".to-search-btn").click( function(event) {
    event.preventDefault();
    $('main').load('/search' + ' #search', "", getFormItems);
  });

  $("#main-page").click( function() {
    event.preventDefault();
    $('main').load('/' + ' #main-page-content', "", getFormItems);
  });
}


// Вставляет слайдеры в поисковой блок
function getFormItems() {

  let sliderEntry = new SearchSlider("#entry-range", "#n-entries-min", "#n-entries-max");
  let sliderText = new SearchSlider("#text-range", "#n-texts-min", "#n-texts-max");

  // Слайдер для частотности конструкции
  $( "#entry-slider-range" ).slider( sliderEntry );

  // Слайдер для частотности текстов
  $( "#text-slider-range" ).slider( sliderText );

  // Перехват поисковых запросов
  $("form#search-form").submit( catchSearchQuery );

}


// Если на старнице с выдачей контестов формул нажали на знак вернуться к началу страницы
function insertEmptyOutputPlaque() {
  let newDiv = `
    <div class="card text-center">
      <div class="card-header">
        Ошибка
      </div>
      <div class="card-body">
        <h5 class="card-title">Примеров на конструкцию не найдено.</h5>
          <p class="card-text">Попробуйте, пожалуйста, другой запрос.</p>
          <a class="btn text-light" href="/"  role="button">Вернуться на главную</a>
      </div>
      </div>
    `;
  $( "#formula-examples" ).append(newDiv);
}


// Конструктор слайдера
function SearchSlider (labelName, minName, maxName) {
  this.range = true;
  this.min = 1;
  this.max = 8;
  this.step = 1;
  this.values = [ 3, 6 ];
  this.create = function() {
      $(labelName).val(" c 3 по 6");
      $(minName).attr("value", 3);
      $(maxName).attr("value", 6);
    };
  this.slide = function (event, ui) {
      let minVal = ui.values[ 0 ];
      let maxVal = ui.values[ 1 ];
      $(labelName).val( "с " + String(minVal) + " по " + String(maxVal));
      $(minName).attr("value", minVal);
      $(maxName).attr("value", maxVal);
    };
}


function MyJsonCallBackF (data) {
    console.log('ajax done');
};  


// Перехват поисковых запросов
function catchSearchQuery() {

    let query_values = $('form#search-form').serialize();
    
    var cur_api_url = API_URL + "/api/formula_search?" + query_values
   
	$.ajax({
  		url: cur_api_url,
  		type: 'GET',
//   		dataType: 'jsonp',
  		jsonp: 'callback',
//   		jsonpCallback: jsonpCallback,
//   		jsonpCallback: 'myCallback',
		success: function( data ) {
			let alpRow = $( "#alphabet-table" );
			alpRow.empty();
     		$("#construction-examples").empty();
     		let alphabet = data.reduce(getFirstLetters, {});
     		Object.entries(alphabet).forEach(insertAlphabet);
    	},
  		error: function(xhr, status, error) {
        	console.log(status + '; ' + error);
        }  		
	});
  
  //  $.get(API_URL + "/api/formula_search?" + query_values, function(data) {
// 
//      let alpRow = $( "#alphabet-table" );
// 
//      alpRow.empty();
// //      alpRow.append("<tr></tr>");
//      $("#construction-examples").empty();
// 
//      let alphabet = data.reduce(getFirstLetters, {});
//      Object.entries(alphabet).forEach(insertAlphabet);
//  });
  return false;
}


// Группируем данные по первой букве
function getFirstLetters(acc, item) { 
  let firstLetter = item.verb_text.slice(0, 1);
  if (!acc.hasOwnProperty(firstLetter)) {
         acc[firstLetter] = [];
       }
  acc[firstLetter].push(item); 
  return acc;
}


// Формируем алфавитные списки
function insertAlphabet(value){

  let key = value[0].toUpperCase();
  let constructions = value[1];
  let newLetter = '<div class="p-2 bd-highlight"><a href="#' + key + '" style="color:#737a71;">' + key + '</a></div>';
  let examplePlace = '<div class="container mb-5 constructions" id="';
  examplePlace += key + '"><h4 class="main-letter">' + key + '</h4></div>';
    
  $("#alphabet-table").append(newLetter);
  $("#construction-examples").append(examplePlace);

  constructions.forEach(makeConstrList, key);
}


// Формируем списки для конктерной буквы
function makeConstrList(item){
 // [{}, {}, {}, {}]
  let key = this.valueOf();
  let link = "formula/" + item.id;
  let constr = '<p lang="is"><a class="text-secondary" href="';
  constr += link + '" target="_blank">';
  constr += item.text + "</a></p>";
  $("#" + key).append(constr);
}
