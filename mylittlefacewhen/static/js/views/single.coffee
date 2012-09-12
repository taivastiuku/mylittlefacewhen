window.SingleView = Backbone.View.extend
  el: "#content"
  initialize: ->
    @template = tpl.get('single')
    @model.on "change", => @render()
    @model.fetch() if @model.isNew() and not @options.firstLoad
    $(window).scrollTop(0)

  events:
    "click .tag": "navigateAnchor"
    "focus #controls div": "activate"
    "blur #controls div": "deactivate"
    "click #editbutton": "editInfo"
    "click .window .close" : "cancel"
    "click #mask" : "cancel"
    "click #single": "random"
    "click .window .report": "report"
    "submit form": "saveInfo"
    "click #flag": "showWindow"

  beforeClose: -> @model.off("change")

  render: ->
    unless @model.isNew() #Still loading data from initialize
      $("#loader").hide()
      current_scroll = $(window).scrollTop() #hax for tagedits
      face = @model.toJSON()
      image = @model.getImage()
      thumb = @model.getThumb(false, true)

      if face.source
        face.source = [{source:face.source}]
      else
        face.source = []
      resizes = []

      resizes.push({size:"huge", image:face.resizes.huge}) if face.resizes.huge
      resizes.push({size:"large", image:face.resizes.large}) if face.resizes.large
      resizes.push({size:"medium", image:face.resizes.medium}) if face.resizes.medium
      resizes.push({size:"small", image:face.resizes.small}) if face.resizes.small

      face.resizes = resizes

      @updateMeta(face)

      to_template =
        artist: face.artist
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
    $("#mask, .window").hide()

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
    reason = $(".window textarea").val()
    return unless reason

    @undelegateEvents()
    $.ajax
      type:"POST"
      url:"/api/v2/flag/"
      contentType: "application/json; charset=utf-8"
      data: '{"reason":"' + reason + '"}'
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
    
    source = event.currentTarget[1].value
    tags = event.currentTarget[0].value.split(",")
    submit_tags = []
    for tag in tags
      submit_tags.push name: $.trim(tag)


    save = =>
      @model.save
        tags: submit_tags
        source: source
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
      .show()

    $(id)
      .css({ top: winH/3, left: winW/2 - $(id).width() / 2 })
      .show()
