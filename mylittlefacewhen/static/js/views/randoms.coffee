window.RandomsView = Backbone.View.extend
    # Endless list of random images
    el: "#content"

    initialize: ->
        @loading = false
        @template = tpl.get("randoms")
        $(window).on "resize.randoms", (event) =>
            @loadMore() if atBottom(500)
        $(window).on "scroll.randoms", (event) =>
            @loadMore() if atBottom(500)

    beforeClose: ->
        $(window).off ".randoms"

    render: ->
        @updateMeta()
        @$el.html Mustache.render(@template, {static_prefix: static_prefix})
        @loadMore()
        return @

    updateMeta: ->
        $("title").html "Random images - MyLittleFaceWhen"
        $("meta[name=description]").attr "content", "Endless list of random pony-related reaction images. Goes on-and-on-and-on-and..."
        $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cherilee-square-300.png"
        $("#cd-layout").remove()
        $("link[rel=image_src]").remove()

    loadMore: ->
        # Similar loadmore to the one in main view
        unless @loading
            @loading = true
            $("#loader").show()
            collection = new FaceCollection()
            collection.fetch
                data: $.param({order_by: "random", limit: 3})
                success: (data) =>
                    _.each collection.models, (model) ->
                        #adding same model twice to a collection causes error
                        app.randFaceList.add(model) unless app.randFaceList.get(model.id)
                        $("#randoms").append new RandomsImage(model:model).render().el

                    $("#loader").hide()
                    @loading = false
                    if data.length > 0
                        @loadMore() if atBottom(500)
                    else
                        $("#loadMore").hide()
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
        image = @getImageBySize(model)

        image = app.getImageService() + image
        
        to_template =
            model: model
            image: image
            static_prefix: static_prefix

        @$el.html Mustache.render(@template, to_template)
        $(@el.firstChild).on "click", @navigateAnchor
        $(@el.firstChild.firstChild).load ->
            $(this).removeClass('fixedHeight')

        return @


    getImageBySize: (data) ->
        #TODO move to model ?
        browser_width = $(document).width()
        
        if data.width > data.height
            if browser_width < 450 and data.resizes.small
                return data.resizes.small
            else if browser_width < 750 and data.resizes.medium
                return data.resizes.medium
              #        else if data.resizes.large
              #  return data.resizes.large
            else
                return data.image

        else
          if browser_width < 320 and data.resizes.small
              return data.resizes.small
          if browser_width < 640 and data.resizes.medium
              return data.resizes.medium
          else if data.resizes.large
              return data.resizes.large
          else
              return data.image
