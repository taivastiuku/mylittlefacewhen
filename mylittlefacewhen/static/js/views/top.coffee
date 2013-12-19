window.TopView = Backbone.View.extend
  el: $("#top")
  initialize: ->
    @template = tpl.get("top")
    @collection = new AdvertCollection()
    KeyboardJS.on 's', null, (event) => $("#searchbar").focus()

  events:
    "focus #topmenu a":"focused"
    "blur #topmenu a":"unfocused"
    "submit #search form": "search"
    "click #topmenu a": "navigateAnchor"
    "click #logo a": "navigateAnchor"
    "click #close-ad": "closeAd"
    "keydown input": "disableShortcuts"
    "keyup input": "disableShortcuts"

  render: ->
    $(@el).html @template #Mustache.render(@template, {})
    @autocomplete $("#searchbar")
    # Ads disabled for now
    #@updateAd()
    return @

  closeAd: (event) ->
    event.preventDefault()
    $("#mainos").slideUp("fast")
    $.cookie('noads', true, {expires: 8, path: '/'})
    return undefined

  updateAd: ->
    return
#    unless $.cookie('noads') or $(window).width() < 700
#      @collection.fetch
#        success: =>
#          $ad = $("#mainos")
#          $ad.find("span").html @collection.models[0].get("htmlad")
#          $ad.slideDown("fast")

    return undefined

  disableShortcuts: (event) ->
    event.stopPropagation()

  search: (event) ->
    event.preventDefault()
    tags = $("#searchbar").val()
    if window.location.pathname.indexOf("/search/") == 0
        # this is not optimal since it breaks 'back' by adding unneeded history entry
        # it is still needed because backbone doesnt seem to understand url parameters
        # TODO fix it better
        app.navigate("/search", {trigger:false})
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

        $.getJSON "/api/v3/tag/", params, (data, textStatus, jdXHR) ->
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
