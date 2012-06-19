window.APIDocView = Backbone.View.extend
    # API documentation page

    el: "#content"

    events: ->
        "click .navigate": "navigateAnchor"

    initialize: ->
        @options.version = "v2" if @options.version == undefined
        @template = tpl.get("apidoc-" + @options.version)
    
    render: ->
        @updateMeta()
        @$el.html @template
        return @

    updateMeta: ->
        $("title").html "API#{@options.version} Documentation - MyLittleFaceWhen"
        $("meta[name=description]").attr "content", "Information about API for mylittlefacewhen. It can be used to fetch data from the service and for maintanence by administrator."
        $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cherilee-square-300.png"
        $("#cd-layout").remove()
        $("link[rel=image_src]").remove()


window.DevelopView = Backbone.View.extend
    # Information page about the develoment, techniques and other stuff 
    # related to the service.
    
    el: "#content"

    initialize: ->
        @template = tpl.get("develop")
   
    events: ->
        "click .navigate": "navigateAnchor"
        "click #mlfw": "random"

    render: ->
        @updateMeta()
        $(@el).html @template
#        for item in $(@el).find(".navigate")
#            $(item).on "click", @navigateAnchor
        return @

    updateMeta: ->
        $("title").html "Information - MyLittleFaceWhen"
        $("meta[name=description]").attr "content", "How and why this service exists. API, feed, etc."
        $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cherilee-square-300.png"
        $("#cd-layout").remove()
        $("link[rel=image_src]").remove()
 
    random: (event) ->
        event.preventDefault()
        app.random()


window.ChangesView = Backbone.View.extend
    # Display a list of changes that have been made to the service.
    
    el: "#content"

    initialize: ->
        @template = tpl.get("changelog")
    
    render: ->
        @updateMeta()
        $(@el).html @template
        return @
        
    updateMeta: ->
        $("title").html "Changelog - MyLittleFaceWhen"
        $("meta[name=description]").attr "content", "List of changes to the service."
        $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cherilee-square-300.png"
        $("#cd-layout").remove()
        $("link[rel=image_src]").remove()
    
