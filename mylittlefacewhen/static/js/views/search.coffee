window.SearchView = Backbone.View.extend
  el: "#content"

  initialize: (data) ->
    @template = tpl.get("search")
    @model = new FaceCollection()



  render: ->
    @updateMeta
    tags = getUrlParam("tags")
    tags = getUrlParam("tag") if not tags
    if not tags
      to_template =
        query: "Search by typing some tags into the searchbox __^"
        static_prefix: static_prefix
      @$el.html Mustache.render(@template, to_template)
      return @
     
    to_template =
      query: tags
      static_prefix: static_prefix
    @$el.html Mustache.render(@template, to_template)
    loader = @$el.children("#loader")
    loader.show()
    
    tags = JSON.stringify(tags.split(","))

    @model.fetch
      data: $.param
        search: tags
        limit: 1000
        order_by: "-id"
      success: (data) =>
        thumbs = @$el.children("#thumbs")
        if @model.models.length == 0
          thumbs.html "No search results"
        else if @model.models.length == 1
          app.navigate("/f/" + @model.models[0].attributes.id + "/", {trigger: true})
        else
          _.each @model.models, (model) ->
            $(thumbs).append new Thumbnail(model:model).render().el

          imgs = $('.lazy')
          if $.browser.webkit
            imgs.removeClass('lazy').lazyload effect: "fadeIn"
          else
            imgs.removeClass('lazy').lazyload()
        loader.hide()

      error: =>
        @$el.children("h2").html "There was an error"
        loader.hide()


    return @


  updateMeta: ->
    $("title").html "#{tags} - MyLittleFaceWhen"
    $("meta[name=description]").attr "content", "Search reslut for pony reaction tag '#{tags}'"
    $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png"
    $("#cd-layout").remove()
    $("link[rel=image_src]").remove()
    $("link[rel=canonical]").remove()

