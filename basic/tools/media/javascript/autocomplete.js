
/*
 * Auto Complete Field
 * Design to be used with the AutoCompleteWidget form field widget.
 */

AutoCompleteWidget = function(field, data) {
  var field = $('#'+field);
  var id_field = field.parent().find('input[type=hidden]');

  function formatItem(item) {
    return item.text;
  }

  function handleResult(e, data, formatted) {
    var span = $('<span class="ac_result"><a href="#'+data.id+'">x</a>'+data.text+'</span>');
    span.insertAfter(field);
    field.val('');

    if (id_field.val()) {
      id_list = id_field.val().split(',');
    }
    else {
      id_list = [];
    }
    id_list.push(data.id)

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

  function parse(data) {
    parsed = [];
    for (var i=0; i<data.length; i++) {
      parsed[parsed.length] = {
        data: data[i],
        value: data[i].text,
        result: data[i].text
      };
    }
    return parsed;
  }

  field.autocomplete(data, {
    matchContains: true,
    formatItem: formatItem,
    parse: parse,
    cacheLength: 0
  }).result(handleResult);

  $('span.ac_result a').live('click', removeResult);
};