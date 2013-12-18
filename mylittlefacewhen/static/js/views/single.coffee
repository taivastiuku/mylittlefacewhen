window.SingleView = Backbone.View.extend
  el: "#content"
  initialize: (options) ->
    @template = tpl.get('single')
    @model.on "change", => @render()
    @model.fetch() if @model.isNew() and not options.firstLoad
    $(window).scrollTop(0)
    KeyboardJS.on 'r', (event) => @random(event)
    KeyboardJS.on 'left', (event) => @previous(event)
    KeyboardJS.on 'right', (event) => @next(event)
    KeyboardJS.on 'h', (event) => @previous(event)
    KeyboardJS.on 'l', (event) => @next(event)
    KeyboardJS.on 'esc', (event) => @cancel(event)

    @updateUsername()

  events:
    "click .tag": "navigateAnchor"
    "focus #controls div": "activate"
    "blur #controls div": "deactivate"
    "click #editbutton": "editInfo"
    "click .window .close" : "cancel"
    "click #mask" : "cancel"
    "click #single": "random"
    "click .window .report": "report"
    "submit #info-edit form": "saveInfo"
    "click #flag": "showWindow"
    "keydown input": "disableShortcuts"
    "keyup input": "disableShortcuts"
    "keydown textarea": "disableShortcuts"
    "keyup textarea": "disableShortcuts"
    "submit #comments form": "comment"

  beforeClose: ->
    @model.off("change")
    KeyboardJS.clear 'r'
    KeyboardJS.clear 'left'
    KeyboardJS.clear 'right'
    KeyboardJS.clear 'h'
    KeyboardJS.clear 'l'
    KeyboardJS.clear 'esc'

  render: ->
    unless @model.isNew() #Still loading data from initialize
      $("#loader").hide()
      current_scroll = $(window).scrollTop() #hax for tagedits
      face = @model.toJSON()
      image = @model.getImage()
      thumb = @model.getThumb(false, true)

      resizes = []
      for size in ["huge", "large", "medium", "small"]
        resizes.push({size:size, image:face.resizes[size]}) if face.resizes[size]
      face.resizes = resizes

      @updateMeta(face)
      @updateUsername()

      to_template =
        face: face
        image: image
        static_prefix: static_prefix
        thumb: thumb
        image_service: app.getImageService()

      @$el.html Mustache.render(@template, to_template)
      $(".single").css "max-height", screen.height
      setTimeout( -> #damn chrome :/
        $(window).scrollTop(current_scroll)
      , 300)


    return @

  updateMeta: (face) ->
    $("title").html face.title + " - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", face.description
    $("#og-image").attr "content", face.image
    if $("#cd-layout") == []
      $("head").append("<meta id='#cd-layout' poperty='cd:layout' content='banner'>")

    image_src = $("link[rel=image_src]")
    if image_src == []
      $("head").append("<link rel='image_src' href='#{face.image}'>")
    else
      image_src.attr("href", face.image)

    canonical = $("link[rel=canonical]")
    if canonical == []
      $("head").append("<link rel='canonical' href='http://mylittlefacewhen.com/f/#{face.id}/'>")
    else
      canonical.attr "href", "http://mylittlefacewhen.com/f/#{face.id}/"

  activate: (event) ->
    $(event.currentTarget).addClass("activated")

  cancel: (event) ->
    event.preventDefault()
    $("#mask, .window").fadeOut("fast")

  deactivate: (event) ->
    $(event.currentTarget).removeClass("activated")

  editInfo: (event) ->
    @$el.find("#info-show").hide()
    @$el.find("#info-edit").show()
    $(document).scrollTop $(document).height()

  random: (event) ->
    event.preventDefault()
    @undelegateEvents()
    @$el.html "<div id='loader'><img src='/static/dash.gif' /></div>"
    $("#loader").show()
    app.random()

  report: (event) ->
    event.preventDefault()
    reason = $(".window textarea").val().replace(/\n/g, "\\n")
    return unless reason
    console.log(@model)
    data = JSON.stringify
      reason: reason
      face: "/api/v3/face/#{@model.get("id")}/"

    @undelegateEvents()
    $.ajax
      type:"POST"
      url: "/api/v3/flag/"
      contentType: "application/json; charset=utf-8"
      data: data
      processData: false
      success: ->
        app.navigate("/f/1221/", true)
      error: ->
        info = $(".window h2")
        info.css("color", "black").css("background-color", "red")
        info.html("An error has ocurred with this report !")


  saveInfo: (event) ->
    event.preventDefault()
    $("#loader").show()
    @$el.find("#info-edit").hide()

    save = =>
      @model.save
        tags: event.currentTarget[0].value
        source: event.currentTarget[1].value
      , wait: true

    if @model.isNew()
      @model.fetch
        success: =>
          save()
    else
      save()

  showWindow: (event) ->
    id = "#dialog"
    winH = $(window).height()
    winW = $(window).width()

    $("#mask")
      .css({ width: winW, height: winH })
      .fadeIn("fast")

    $(id)
      .css({ top: winH/3, left: winW/2 - $(id).width() / 2 })
      .fadeIn("fast")

  previous: (event) -> @gotoDir(event, "-id", "lt")

  next: (event) -> @gotoDir(event, "id", "gt")

  gotoDir: (event, order, dir) ->
    col = new FaceCollection()
    params =
      order_by: order
      limit: 1
      accepted: true
      removed: false
    params["id__#{dir}"] = @model.get("id")

    col.fetch
      data: params
      success: (data) =>
        return undefined unless col.length > 0
        app.navigate("f/#{col.models[0].get("id")}/", trigger:true)

  disableShortcuts: (event) ->
    event.stopPropagation()

  comment: (event) ->
    event.preventDefault()
    data = {}
    _.each $(event.target).serializeArray(), (input) ->
      data[input.name] = input.value

    localStorage.setItem("username", data["username"])

    comment = new Comment(data)
    comment.save null,
      success: (model, response, options) =>
        window.location.reload()
    console.log(data)

  updateUsername: ->
    username = localStorage.getItem("username")
    if username
      @$el.find("#comments input[name=username]").val(username)
