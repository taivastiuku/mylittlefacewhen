window.APIDocView = Backbone.View.extend
  # API documentation page
  el: "#content"
  initialize: (options) ->
    console.log options
    if options.version == undefined
        @version = "v3"
    else
        @version = options.version
    @title = "API#{@version} Documentation - MyLittleFaceWhen"
    @description = "Information about API for mylittlefacewhen. It can be used to fetch data from the service and for maintanence by administrator."
    @template = tpl.get("apidoc-" + @version)

  events: ->
    "click .navigate": "navigateAnchor"

  render: ->
    @updateMeta(@title, @description)
    @$el.html @template
    return @


window.DevelopView = Backbone.View.extend
  # Information page about the develoment, techniques and other stuff
  # related to the service.
  el: "#content"
  initialize: ->
    console.log "hello"
    @title = "Information - MyLittleFaceWhen"
    @description = "How and why this service exists. API, feed, etc."
    @template = tpl.get("develop")

  events: ->
    "click .navigate": "navigateAnchor"
    "click #mlfw": "random"

  render: ->
    @updateMeta(@title, @description)
    $(@el).html @template
    return @

  random: (event) ->
    event.preventDefault()
    app.random()


window.ChangesView = Backbone.View.extend
  # Display a list of changes that have been made to the service.
  el: "#content"
  initialize: ->
    @title = "Changelog - MyLittleFaceWhen"
    @description = "List of changes to the service."
    @template = tpl.get("changelog")

  render: ->
    @updateMeta(@title, @description)
    $(@el).html @template
    return @
