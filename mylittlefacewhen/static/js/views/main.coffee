window.MainView = Backbone.View.extend
  # The main views that list newest images
  el: "#content"
  initialize: (options) ->
    @title = "Pony Reaction Pictures - MyLittleFaceWhen"
    @description = "Express yourself with ponies."
    @template = tpl.get('main')
    @offset = 0 if not @offset
    @loading = false
    @order_by = options.order_by
    $(window).on "resize.main", (event) => @loadMore() if atBottom(300)
    $(window).on "scroll.main", (event) => @loadMore() if atBottom(300)

  events:
    "click #loadMore": "loadMore"
    "click .thumb a": "navigateAnchor"

  render: ->
    @updateMeta(@title, @description)
    @$el.html Mustache.render(@template,{static_prefix: static_prefix, message: []})
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

  loadMore: ->
    #load more thumbnails
    unless @loading
      @loading = true
      $("#loader").show()
      collection = new FaceCollection()
      collection.fetch
        data:
          offset: @offset
          order_by: @order_by
          accepted: true
          removed: false
        success: (data) =>
          if app.currentPage == @
              collection.each (model) ->
                $("#thumbs").append new Thumbnail(model:model).render().el

              imgs = $('.lazy')
              imgs.removeClass('lazy').lazyload()

              $("#loader").hide()
              @collection.add collection.models
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
    $(window).off "resize.main"
    $(window).off "scroll.main"

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
    @title = "Pony Reaction Pictures - MyLittleFaceWhen"
    @description = "Express yourself with ponies."
    @template = tpl.get('main')

  render: ->
    @updateMeta(@title, @description)
    to_template =
      static_prefix: static_prefix
      message: [ {message: "Unreviewed images"}, {message:"Uploaded images may take a few seconds to appear here and duplicates may get automatically removed."} ]

    @$el.html Mustache.render(@template, to_template)

    $("#loader").show()
    $("#loadMore").hide()

    @collection.fetch
      data:
        accepted: false
        removed: false
        limit: 1000
        order_by: "-id"
      success: (data) =>
        @collection.each (model) ->
          $("#thumbs").append new Thumbnail(model:model).render().el

        imgs = $('.lazy')
        imgs.removeClass('lazy').lazyload()

        $("#loader").hide()
    return @


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
    model.thumb = @model.getThumb(@webp)
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
