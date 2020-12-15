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
        console.log("caret-down")
      } else if ($("#caret-sigh").hasClass("bi-caret-down")) {
          $("#caret-sigh").attr("class", "bi-caret-up");
          $("path", this).attr("d", 
            "M3.204 11L8 5.519 12.796 11H3.204zm-.753-.659l4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z");
          console.log("caret-up")};
    }
    );


    let condition1 = (/\/formula\//.test(this.location.pathname));
    let condition2 = ($( ".formula-example" ).length <= 0);

    // Если это страница контекста формулы и нет никаких данных, вставить предупреждалку с ошибкой
    if (condition1 && condition2) {
      insertEmptyOutputPlaque();
    };


    // Если нажали на главную страницу, открываем ее
    $("#main-page").click( function() {
      window.location.replace("/");
    });


    // Если на старнице с выдачей контестов формул нажали на знак вернуться к началу страницы
    $(".caret-up-btn").click( function() {
      window.location.replace("#");
    });


    // Если нажали на поисковую страницу, открываем ее
    $(".to-search-btn").click( function() {
      window.location.replace("/search");
    });


    var sliderEntry = new mySlider("#entry-range", "#n-entries-min", "#n-entries-max");
    var sliderText = new mySlider("#text-range", "#n-texts-min", "#n-texts-max");


    // Слайдер для частотности конструкции
    $( "#entry-slider-range" ).slider( sliderEntry );

    // Слайдер для частотности текстов
    $( "#text-slider-range" ).slider( sliderText );
  

    // Перехват поисковых запросов
    $("form#search-form").submit( catchSearchQuery );

  }
);


// Если на старнице с выдачей контестов формул нажали на знак вернуться к началу страницы
function insertEmptyOutputPlaque() {
  var newdiv = `
    <div class="card text-center">
      <div class="card-header">
        Ошибка
      </div>
      <div class="card-body">
        <h5 class="card-title">Примеров на конструкцию не найдено.</h5>
          <p class="card-text">Попробуйте, пожалуйста, другой запрос.</p>
          <a class="btn text-light to-search-btn" role="button">Вернуться к поиску</a>
      </div>
      </div>
    `
  $( "#formula-examples > div" ).append(newdiv);
};


// Конструктор слайдера
function mySlider (labelName, minName, maxName) {
  this.range = true;
  this.min = 1;
  this.max = 8;
  this.step =1;
  this.values = [ 3, 6 ];
  this.create = function() {
      $(labelName).val(" c 3 по 6");
      $(minName).attr("value", 3);
      $(maxName).attr("value", 6);
    };
  this.slide = function (event, ui) {
      var minVal = ui.values[ 0 ];
      var maxVal = ui.values[ 1 ];
      $(labelName).val( "с " + String(minVal) + " по " + String(maxVal));
      $(minName).attr("value", minVal);
      $(maxName).attr("value", maxVal);
    };
};


// Перехват поисковых запросов
function catchSearchQuery() {

  var query_values = $('form#search-form').serialize();

    $.get("api/formula_search?" + query_values, function(data) {
      var alpRow = $( "#alphabet-table > tbody > tr" );

      alpRow.empty();
      alpRow.append("<tr></tr>");
      $("#construction-examples").empty();

      var alphabet = data.reduce(getFirstLetters, {});
      Object.entries(alphabet).forEach(insertAlphabet);
  });
  return false;
};


// Группируем данные по первой букве
function getFirstLetters(acc, item) { 
  firstLetter = item['text'].slice(0, 1); 
  if (!acc.hasOwnProperty(firstLetter)) {
         acc[firstLetter] = [];
       }
  acc[firstLetter].push(item); 
  return acc;
};


// Формируем алфавитные списки
function insertAlphabet(value, index, array){

  var key = value[0].toUpperCase();
  var constructions = value[1];
  var newLetter = '<th scope="col"><a href="#' + key + '" style="color:#737a71;">' + key + "</a></th>";
  var exmlPlace = '<div class="container mb-5 constructions" id="';
  exmlPlace += key + '"><h4 class="main-letter">' + key + '</h4></div>';
    
  $("#alphabet-table > tbody > tr").append(newLetter);
  $("#construction-examples").append(exmlPlace);

  constructions.forEach(makeConstrList, key);
};


// Формируем списки для конктерной буквы
function makeConstrList(item){
 // [{}, {}, {}, {}]
  var key = this.valueOf();
  var link = "formula/" + item['id'];
  var constr = '<p lang="is"><a class="text-secondary" href="';
  constr += link + '" target="_blank">';
  constr += item['text'] + "</a></p>";
  $("#" + key).append(constr);
};












