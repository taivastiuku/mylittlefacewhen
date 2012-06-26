window.SingleView = Backbone.View.extend
  el: "#content"
  initialize: ->
    @template = tpl.get('single')

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

  render: ->
    @fetcher @renderIt()
    return @

  fetcher: (callback) ->
    if @model.get("not_fetched")
      @model.fetch
        success: =>
          @model.set("not_fetched", false)
          callback()
    else
      callback()

    return undefined

  renderIt: ->
    face = @model.toJSON()
    image = @model.getImage()
    thumb = @model.getThumb()

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

    to_template =
      face: face
      image: image
      static_prefix: static_prefix
      thumb: thumb
      image_service: app.getImageService()
    
    @$el.html Mustache.render(@template, to_template)
    $(".single").css "max-height", screen.height

    $(window).scrollTop(0)

    tags = ""
    for tag in face.tags
      tags += tag.name + ", "
    @updateMeta(face, tags)


    return @

  updateTags: (tags) ->
    taglist = $(@el).find("#tags")
    taglist.html("")
    _.each tags, (tag) ->
      taglist.append(new TagView(model: new Tag(name:tag.name)).render().el) unless tag.name == ""


  updateMeta: (face, tags) ->
    $("title").html "Image #{face.id} - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", "Reaction containing: #{tags}"
    $("#og-image").attr "content", face.image
    $("head").append("<meta id='#cd-layout' poperty='cd:layout' content='banner'>") if $("#cd-layout") == []
    $("head").append("<link rel='image_src' href='#{face.image}'>") if $("link[rel=image_src]") == []

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
    tags = event.currentTarget[0].value.split(",")
    i = 0
    while i < tags.length
      tags[i] = $.trim(tags[i])
      i++
    $("#loader").show()

    @$el.find("#info-edit").hide()
    
    submit_tags = []
    _.each tags, (tag) ->
      submit_tags.push {"name": tag}

    if @model.isNew()
      @fetcher =>
        @model.save {tags: submit_tags,source: event.currentTarget[1].value},
          success: =>
            @updateTags submit_tags
            $("#source").html(event.currentTarget[1].value)

            show = ->
              $("#loader").hide()
              $("#info-show").show()

            window.setTimeout show, 1000

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
