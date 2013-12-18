window.SearchView = Backbone.View.extend
  el: "#content"

  initialize: (data) ->
    @template = tpl.get("search")
    @model = new FaceCollection()

  render: ->
    tags = getUrlParam("tags") or getUrlParam("tag")
    @updateMeta("Search for '#{tags}' - MyLittleFaceWhen", "Search result for pony reaction tag '#{tags}'")

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

    @model.fetch
      data:
        tags__all: tags
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
          imgs.removeClass('lazy').lazyload()
        loader.hide()

      error: =>
        @$el.children("h2").html "There was an error"
        loader.hide()

    return @
