window.TopView = Backbone.View.extend
  el: $("#top")
  initialize: ->
    @template = tpl.get("top")
    @collection = new AdvertCollection()

  events:
    "focus #topmenu a":"focused"
    "blur #topmenu a":"unfocused"
    "submit #search form": "search"
    "click #topmenu a": "navigateAnchor"
    "click #logo a": "navigateAnchor"
    "click #close-ad": "closeAd"

  render: ->
    $(@el).html @template #Mustache.render(@template, {})
    @autocomplete $("#searchbar")
    @updateAd()
    return @

  closeAd: (event) ->
    event.preventDefault()
    $("#mainos").hide("fast")
    $.cookie('noads', true, {expires: 8, path: '/'})
    return undefined

  updateAd: ->
    unless $.cookie('noads') or $(window).width() < 700
      @collection.fetch
        success: =>
          $ad = $("#mainos")
          $ad.find("span").html @collection.models[0].get("htmlad")
          $ad.show("fast")

    return undefined



  search: (event) ->
    event.preventDefault()
    tags = $("#searchbar").val()
    app.navigate("/search/?tag=#{tags}", {trigger:true})

  focused: (event) ->
    $(event.currentTarget.firstChild).addClass "focused"

  unfocused: (event) ->
    $(event.currentTarget.firstChild).removeClass "focused"

  autocomplete: (element) ->
    element.autocomplete
      source: (request, response) ->
        params =
          name__contains: ac_extractLast(request.term)
          limit: 30

        $.getJSON "/api/v2/tag/", params, (data, textStatus, jdXHR) ->
          d = []
          _.each data.objects, (tag) ->
            d.push tag.name
          response(d, textStatus, jdXHR)

      search: ->
        # custon minLength
        term = ac_extractLast(@value)
        false  if term.length < 2

      focus: ->
        # prevents value inserted on focus
        false

      select: (event, ui) ->
        terms = ac_split(@value)
        # remove the current input
        terms.pop()
        # add the selected item
        terms.push ui.item.value
        # add placeholder to get the comma-and-space at the end
        terms.push ""
        @value = terms.join(", ")
        false

#TODO move these somewhere
ac_split = (val) ->
  val.split /,\s*/

ac_extractLast = (term) ->
  ac_split(term).pop()






