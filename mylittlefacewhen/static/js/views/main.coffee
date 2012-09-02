window.MainView = Backbone.View.extend
  # The main views that list newest images

  el: "#content"

  initialize: ->
    @template = tpl.get('main')
    #@meta = tpl.get('meta')
    #@metadata =
    #  title: "Pony Reaction Pictures"
    #  description: "Lots of well-tagged pony reaction images, add yours!"
    #  default_image: "#{static_prefix}cheerilee-square-300.png"
    #  static_prefix: static_prefix

    @offset = 0 if not @offset
    @loading = false
    $(window).on "resize.main", (event) =>
      @loadMore() if atBottom(300)
    $(window).on "scroll.main", (event) =>
      @loadMore() if atBottom(300)

  events:
    "click #loadMore": "loadMore"
    "click .thumb a": "navigateAnchor"

#  remove: ->
#    Backbone.View::remove.call @

  render: ->
    @updateMeta()
    @$el.html Mustache.render(@template,{static_prefix: static_prefix, message: []})
    #$("head").html Mustache.render(@meta, @metadata)
    if @html
      # load html from memory if user has visited the main view
      # during current visit
      thumbs = $(@$el.find("#thumbs"))
      thumbs.append(@html)
      _.each thumbs.find("a"), (img) =>
        $(img.firstChild)
          .addClass("fixedWidth")
          .load ->
            if $(this).attr("src") != '/static/empty.gif'
              $(this).removeClass('fixedWidth')

    #scroll to last position if user has visited main view during current visit
    setTimeout("$(window).scrollTop(#{@scroll});", 100) if @scroll
    @loadMore()
    return @

  updateMeta: ->
    $("title").html "Pony Reaction Pictures - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", "Lots of well-tagged pony reaction images."
    $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png"
    $("#cd-layout").remove()
    $("link[rel=image_src]").remove()
    $("link[rel=canonical]").remove()

  
  loadMore: ->
    #load more thumbnails
    unless @loading
      @loading = true
      $("#loader").show()
      collection = new FaceCollection()
      collection.fetch
        data: $.param({offset:@offset, order_by:"-id", accepted:true})
        success: (data) =>
          _.each collection.models, (model) ->
            $("#thumbs").append new Thumbnail(model:model).render().el

          imgs = $('.lazy')
          if $.browser.webkit
            imgs.removeClass('lazy').lazyload effect: "fadeIn"
          else
            imgs.removeClass('lazy').lazyload()

          $("#loader").hide()
          @model.add collection.models
          @offset += 20
          @loading = false
          if data.length > 0
            @loadMore() if atBottom(300)
          else
            $("#loadMore").hide()
        error: ->
          $("#loader").hide()
          loading = false


  beforeClose: ->
    # Clean up a few event handlers and save current state and position of 
    # the page
    $(window).off ".main"
    _.each $(".fixedWidth"), (img) ->
       $(img).removeClass("fixedWidth").attr("src", img.getAttribute("data-original"))

    window.MainView::html = $("#thumbs").html()
    window.MainView::offset = @offset
    window.MainView::scroll = $(window).scrollTop()
  



window.UnreviewedView = Backbone.View.extend
  # Unreviewed images, pretty much the same as main view except all 
  # images are fetched.

  el: "#content"

  initialize: ->
    @template = tpl.get('main')

  render: ->
    @updateMeta()
    to_template =
      static_prefix: static_prefix
      message: [ {message: "unreviewed images"} ]

    @$el.html Mustache.render(@template, to_template)

    $("#loader").show()
    $("#loadMore").hide()

    @model.fetch
      data: $.param
        accepted: false
        limit: 1000
        order_by: "-id"
      success: (data) =>
        _.each @model.models, (model) ->
          $("#thumbs").append new Thumbnail(model:model).render().el

        imgs = $('.lazy')
        if $.browser.webkit
          imgs.removeClass('lazy').lazyload effect: "fadeIn"
        else
          imgs.removeClass('lazy').lazyload()

        $("#loader").hide()
    return @

  updateMeta: ->
    $("title").html "Pony Reaction Pictures - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", "Lots of well-tagged pony reaction images."
    $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png"
    $("#cd-layout").remove()
    $("link[rel=image_src]").remove()
    $("link[rel=canonical]").remove()


window.Thumbnail = Backbone.View.extend
  # Not sure if some of this functionality should be in the model.
  
  tagName: "span"
  className: "thumb"

  events:
    "click .thumb a": "navigateAnchor"

  initialize: ->
    @template = tpl.get('thumbnail')
    @detectWebp() if @webp == undefined
    
  render: ->
    model = @model.toJSON()

    if model.thumbnails.png
      model.thumb = model.thumbnails.png
    else if @webp and model.thumbnails.webp
      model.thumb = model.thumbnails.webp
    else
      model.thumb = model.thumbnails.jpg
    
    model.thumb = app.getImageService() + model.thumb if model.thumb and model.accepted

    if model.thumbnails.gif
      gif = app.getImageService() + model.thumbnails.gif if model.accepted

      model.gifstring = " onMouseOver='this.src=\"" + gif + "\";' onMouseOut='this.src=\"" + model.thumb + "\";'"
    else
      model.gifstring = ""

    @$el.html Mustache.render(@template, {model: model})

    $(@el.firstChild.firstChild).load ->
      if $(this).attr("src") != "#{ static_prefix }empty.gif"
        $(this).removeClass('fixedWidth')

    return @

  detectWebp: ->
    # Detect only once and remember it the whole session.
    # Only Chrome >= 8 supporsts but older chromes are almost non-existant
    # TODO Opera >= 11.10 supports wepb
    # TODO some androids support webp
    # TODO Feature detection instead of browser detection if there is an
    #    elegant solution.
    @webp = navigator.userAgent.toLowerCase().indexOf('chrome') > -1
    window.Thumbnail::webp = @webp
