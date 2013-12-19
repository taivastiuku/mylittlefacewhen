window.RandomsView = Backbone.View.extend
  # Endless list of random images
  el: "#content"

  initialize: ->
    @title = "Random images - MyLittleFaceWhen"
    @description = "Endless list of random pony-related reaction images. Goes on-and-on-and-on-and..."
    @template = tpl.get("randoms")
    @loading = false
    $(window).on "resize.randoms", (event) => @loadMore() if atBottom(500)
    $(window).on "scroll.randoms", (event) => @loadMore() if atBottom(500)

  beforeClose: ->
    $(window).off "resize.randoms"
    $(window).off "scroll.randoms"

  render: ->
    @updateMeta(@title, @description)
    @$el.html Mustache.render(@template, {static_prefix: static_prefix})
    @loadMore()
    return @

  loadMore: ->
    # Similar loadmore to the one in main view
    unless @loading
      @loading = true
      $("#loader").show()
      collection = new FaceCollection()
      collection.fetch
        data:
          order_by: "random"
          limit: 3
          accepted: true
          removed: false
        success: (data) =>
          _.each collection.models, (model) ->
            #adding same model twice to a collection causes error
            app.randFaceList.add(model) unless app.randFaceList.get(model.id)
            $("#randoms").append new RandomsImage(model:model).render().el

          $("#loader").hide()
          #Timeout prevents client from making multiple queries
          setTimeout( =>
            @loading = false
            if data.length > 0
              @loadMore() if atBottom(500) and app.currentPage == @
            else
              $("#loadMore").hide()
          , 1000)
        error: ->
          $("#loader").hide()
          @loading = false


window.RandomsImage = Backbone.View.extend
  # Image in randoms view

  tagName: "div"
  className: "listimage"

  initialize: ->
    @template = tpl.get("randomsImage")

  render: ->
    model = @model.toJSON()
    image = app.getImageService() + @model.getImage(640)

    to_template =
      model: model
      image: image
      static_prefix: static_prefix

    @$el.html Mustache.render(@template, to_template)
    $(@el.firstChild).on "click", @navigateAnchor
    $(@el.firstChild.firstChild).load ->
      $(this).removeClass('fixedHeight')

    return @
