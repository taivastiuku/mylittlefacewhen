window.TagsView = Backbone.View.extend
  el: "#content"

  tags: [
    "applejack"
    "fluttershy"
    "pinkie pie"
    "rainbow dash"
    "rarity"
    "twilight sparkle"
    "princess celestia"
    "princess luna"
    "spike"
    "derpy hooves"
    "trixie"
    "animated"
    "transparent"
    "fanart"
    "screenshot"
    "untagged"
    "yes"
    "do want"
    "no"
    "do not want"
    "creepy"
    "omg"
    "lol"
    "rage"
    "u mad"
    "u jelly"
    "do it filly"
    "hug"
  ]

  events:
    "click .thumb a": "navigateAnchor"
    "click #tagcloud a": "navigateAnchor"

  initialize: ->
    @template = tpl.get("tags")
    @tagsItem_template = tpl.get("tagsItem")

  render: ->
    @updateMeta()
    if @collection.models.length == 0
      @collection.fetch
        data:
          limit: 10000
        success: =>
          @renderIt()
    else
      @renderIt()

    return @
  

  renderIt: ->
    data = @collection.toJSON()
    $(@el).html Mustache.render(@template, models: data)

    $tags = $("#tags")
    for tag in @tags
      tagsItem = $(Mustache.render(@tagsItem_template,tag:tag))
      $tags.append tagsItem
      face = new FaceCollection()
      face.fetch
        data:
          search: JSON.stringify [tag]
          order_by: "random"
          limit: 1
        success: (data) =>
          thumb = new Thumbnail(model:face.models[0]).render()
          tagsItem.children("div").append thumb.el.firstChild

          imgs = $('.lazy')
          if $.browser.webkit
            imgs.removeClass('lazy').lazyload effect: "fadeIn"
          else
            imgs.removeClass('lazy').lazyload()
  
  updateMeta: ->
    $("title").html "Tagcloud and popular tags - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", "All tags known by the service and some of the most frequently needed ones with random pictures."
    $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png"
    $("#cd-layout").remove()
    $("link[rel=image_src]").remove()
    $("link[rel=canonical]").remove()

window.TagView = Backbone.View.extend
  tagName: "span"

  events:
    "click a": "navigateAnchor"

  initialize: ->
    @template = tpl.get("tag")

  render: ->
    $(@el).html Mustache.render(@template, name: @collection.get("name"))
    return @
