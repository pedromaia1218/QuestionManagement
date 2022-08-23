$(document).ready(function () {
  var max_input_fields = 500;
  var add_input = $(".add-input");
  var input_wrapper = $(".input-wrapper");
  var new_input =
    '<div><input class="form-control" type="text" name="question" id="question" placeholder="Coloque aqui a pergunta" /><a href="javascript:void(0);" class="remove-input" title="Remover pergunta"><h5><i class="bi bi-dash-square-fill"></i></h5></a></div>';
  var add_input_count = 1;
  $(add_input).click(function () {
    if (add_input_count < max_input_fields) {
      add_input_count++;
      $(input_wrapper).append(new_input);
    }
  });
  $(input_wrapper).on("click", ".remove-input", function (e) {
    e.preventDefault();
    $(this).parent("div").remove();
    add_input_count--;
  });
});

$(document).ready(function () {
  var max_input_fields = 500;
  var add_context = $(".add-context");
  var context_wrapper = $(".context-wrapper");
  var new_context =
    '<div><input class="form-control" type="text" name="context" id="context" placeholder="Coloque aqui o contexto" /><a href="javascript:void(0);" class="remove-context" title="Remover contexto"><h5><i class="bi bi-dash-square-fill"></i></h5></a></div>';
  var add_input_context = 1;
  $(add_context).click(function () {
    if (add_input_context < max_input_fields) {
      add_input_context++;
      $(context_wrapper).append(new_context);
    }
  });
  $(context_wrapper).on("click", ".remove-context", function (e) {
    e.preventDefault();
    $(this).parent("div").remove();
    add_input_context--;
  });
});

function exportALL(){
    window.location = '/export';
}

function exportNEW(){
  window.location = '/export?new=true';
}