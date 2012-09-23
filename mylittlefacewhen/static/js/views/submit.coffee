window.SubmitView = Backbone.View.extend
  el: "#content"
  initialize: ->
    @title = "Submit Images - MyLittleFaceWhen"
    @descripition = "Upload more images to the service"
    @template = _.template tpl.get("submit")

  events:
    "dragover #dropzone": "handleDragover"
    "drop #dropzone" : "handleDrop"
    "change #files" : "handleChoose"
    "click #upload" : "upload"
    "click #instructions button" : "toggleInstructions"
    "click #to-unreviewed a" : "navigateAnchor"

  render: ->
    @updateMeta()
    $(@el).html @template({static_prefix:static_prefix})
    return @

  handleChoose: (event) ->
    @handleFiles event.target.files

  handleDragover: (event) ->
    event = event.originalEvent
    event.stopPropagation()
    event.preventDefault()
    event.dataTransfer.dropEffect = "copy"

  handleDrop: (event) ->
    event = event.originalEvent
    event.stopPropagation()
    event.preventDefault()
    @handleFiles event.dataTransfer.files

  handleFiles: (files) ->
    updates = []
    for file in files when file.type.match("image.*")
      item =
        "image":file
      updates.push(item)

    thumbs = $(@el).find("#upload_list ul")
    _.each updates, (update) ->

      reader = new FileReader()
      reader.onload =
        do (update) ->
          (event) ->
            item = new SubmitItemView().render(update.image, event.target.result)
            $("#upload_list ul").append(item.el)

      reader.readAsDataURL update.image

    $("#upload").show()

  upload: (event) ->
    @undelegateEvents()
    upload_button =  event.currentTarget
    $(upload_button)
      .find("span")
        .html("uploading")
    $("#loader").show()

    _.each $("#upload_list li"), (item) ->
      tags = $(item).find(".tags").val()
      if $(item).find("input[name=transparent]")[0].checked
        tags += ", transparent"
      if $(item).find("input[name=fanart]")[0].checked
        tags += ", fanart"
      if $(item).find("input[name=screenshot]")[0].checked
        tags += ", screenshot"
      source = $(item).find(".source").val()

      img = $(item).find("img")

      face = new Face
        name: img.attr("title")
        image_data: img.attr("src")
        tags: tags
        source: source

      face.save undefined,
        success: ->
          $(item).remove()
          if $("#upload_list ul").children().length == 0
            app.navigate "/unreviewed/", true
        error: ->
          $(item).find(".info")
            .addClass("error")
            .css("color", "black")
            .css("background-color", "red")
            .html("An error has ocurred with this image")

  toggleInstructions: (event) ->
    $("#instructions div").toggle()


window.SubmitItemView = Backbone.View.extend
  tagName: "li"

  initialize: ->
    @template = tpl.get("submitItem")

  events:
    "click .controls": "remove"

  render: (image, imageURL) ->
    $(@el).html Mustache.render(@template,{image:image, imageURL:imageURL})
    $.get "/api/v2/detect/?filename=" + image.name,
      (data) =>
        $(@el).find(".tags").val(data.tags)
        $(@el).find(".source").val(data.source)

    return @

