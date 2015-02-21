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

  initialize: ->
    @title = "Tagcloud and popular tags - MyLittleFaceWhen"
    @description = "All tags known by the service and some of the most frequently needed ones with random pictures."
    @template = tpl.get("tags")
    @tagsItem_template = tpl.get("tagsItem")

  events:
    "click .thumb a": "navigateAnchor"
    "click #tagcloud a": "navigateAnchor"

  render: ->
    @updateMeta(@title, @description)
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
    _.each @tags, (tag) =>
      tagsItem = $(Mustache.render(@tagsItem_template,tag:tag))
      $tags.append tagsItem
      face = new FaceCollection()
      face.fetch
        data:
          tags__all: tag
          order_by: "random"
          removed: false
          accepted: true
          limit: 1
        success: (data) =>
          thumb = new Thumbnail(model:face.models[0]).render()
          tagsItem.children("div").append thumb.el.firstChild

          imgs = $('.lazy')
          imgs.removeClass('lazy').lazyload()


window.TagView = Backbone.View.extend
  tagName: "span"
  initialize: -> @template = tpl.get("tag")
  events:
    "click a": "navigateAnchor"
  render: ->
    $(@el).html Mustache.render(@template, name: @collection.get("name"))
    return @
