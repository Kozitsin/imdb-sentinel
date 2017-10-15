window.CLASSES = ["Negative", "Positive"]
window.CSS_CLASSES = ["danger", "success"]

var progressBar = {
  show: function() {
    $(".progress").fadeIn();
  },
  hide: function() {
    $(".progress").hide();
  }
};

var prediction = {
  set: function(q, predictedValue, predictedClass) {
    $("#predicted_class").text(CLASSES[predictedClass]);
    $("#predicted_value").text(predictedValue);
    $("#predicted_query").text(q);
    prediction.toggleClasses(predictedClass);
  },
  toggleClasses: function(predictedClass) {
    $("#prediction").removeClass("alert-" + CSS_CLASSES[1 - predictedClass]);
    $("#prediction").addClass("alert-" + CSS_CLASSES[predictedClass]);
  },
  show: function() {
    $("#prediction").fadeIn();
  },
  hide: function() {
    $("#prediction").hide();
  }
};

var examples = {
  show: function() {
    $(".examples").fadeIn(1500);
  },
  add: function(q, l1_predicted, l2_predicted, real) {
    $line = $("<tr>")
    $div = $("<div>").html(q)
    $line.append($("<td class='text'>").text($div.text()));
    $line.append(examples.classCell(l1_predicted));
    $line.append(examples.classCell(l2_predicted));
    $line.append(examples.classCell(real));
    $(".example_items").append($line);
  },
  addAll: function(items) {
    $.each(items, function(i, item){
      l1_predicted = parseInt(item.l1_predicted);
      l2_predicted = parseInt(item.l2_predicted);
      real = parseInt(item.real);
      examples.add(item.q, l1_predicted, l2_predicted, real);
    });
  },
  classCell: function(value){
    return $("<td>").text(CLASSES[value]).addClass(CSS_CLASSES[value]);
  }
}

var statistics = {
  show: function() {
    $(".statistics").fadeIn(1500);
  },
  add: function(item) {
    $line = $("<tr>")
    $div = $("<div>").html(item.name)
    $line.append($("<td class='text'>").text($div.text()));
    $line.append($("<td class='text'>").text(item.accuracy));
    $line.append($("<td class='text'>").text(item.errors.true_positives));
    $line.append($("<td class='text'>").text(item.errors.true_negatives));
    $line.append($("<td class='text'>").text(item.errors.false_positives));
    $line.append($("<td class='text'>").text(item.errors.false_negatives));
    $(".statistic_items").append($line);
  },
  addAll: function(items) {
    $.each(items, function(i, item){
      statistics.add(item);
    });
  }
}

$(function(){
  $("#predict_form").submit(function(e){
    e.preventDefault();
    prediction.hide();
    progressBar.show();

    $.getJSON("/predict",  $(this).serialize()).
      always(function(){
        progressBar.hide();
      }).
        done(function(data) {
          var predictedClass = parseInt(data.predicted_class);
        prediction.set(data.q, data.prediction, predictedClass);
        prediction.show();
      });
  });

  $.getJSON("/examples").done(function(data) {
    examples.addAll(data.items);
    examples.show()

    $("td.text").click(function(){
      $(this).toggleClass("hover", 10000)
    });
  });

  $.getJSON("/test").done(function(data) {
    statistics.addAll(data.items);
    statistics.show()
  });
});
