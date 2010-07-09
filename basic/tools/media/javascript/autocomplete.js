
/*
 * Auto Complete Field
 * Design to be used with the AutoCompleteWidget form field widget.
 */

AutoCompleteWidget = function(field, data) {
  var field = $('#'+field);
  var id_field = field.parent().find('input[type=hidden]');

  function renderItem(ul, item) {
    return $('<li></li>')
      .data('item.autocomplete', item)
      .append('<a>'+item.text+'</a>')
      .appendTo(ul);
  }

  function handleResult(e, ui) {
    var span = $('<span class="ui-autocomplete-result"><a href="#'+ui.item.id+'">x</a>'+ui.item.text+'</span>');
    span.insertAfter(field);
    field.val('');

    if (id_field.val()) {
      id_list = id_field.val().split(',');
    }
    else {
      id_list = [];
    }
    id_list.push(ui.item.id)

    id_field.val(id_list.join(','));
  }

  function removeFromArray(value, array) {
    for (var i=0; i<array.length; i++) {
      if (array[i] == value) {
        array.splice(i, 1);
      }
    }
    return array;
  }

  function removeResult(e) {
    var result = $(this).parent();
    var id = this.hash.slice(1);
    var id_list = id_field.val().split(',');
    var new_id_list = removeFromArray(id, id_list);
    id_field.val(new_id_list.join(','));
    result.remove();
  }

  field.autocomplete({
    source: data,
    select: handleResult,
    delay: 200
  }).data('autocomplete')._renderItem = renderItem;

  $('span.ui-autocomplete-result a').live('click', removeResult);
};