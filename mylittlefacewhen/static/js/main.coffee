# Allow global access to app
app = undefined

# Some views need to clean up before close.
Backbone.View::close = ->
  #console.log "Closing view " + this
  @beforeClose() if @beforeClose
#  @remove()
  @undelegateEvents()


Backbone.View::updateMeta = (title, description) ->
    $("title").html title
    $("meta[name=description]").attr "content", description
    $("#og-image").attr "content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png"
    $("#cd-layout").remove()
    $("link[rel=image_src]").remove()
    $("link[rel=canonical]").remove()


Backbone.View::navigateAnchor = (event) ->
  # Make links work with backbone.js
  event.preventDefault()
  app.navigate(event.currentTarget.getAttribute("href"), {trigger: true})


AppRouter = Backbone.Router.extend
  initialize: ->
    # for some reason this tracks all pages twice
    # @bind 'all', @_trackPageview

    # TODO Could these infused as one?
    @faceList = new FaceCollection()      # loaded from main view
    @randFaceList = new FaceCollection()  # loaded from randoms
    @randomQueue = new FaceCollection()   # cache for randomly loaded images

    @tagList = new TagCollection()
    @firstLoad = if window.location.hash then false else true

    # Client-side load balancing, list services and pick the fastest one.
    # All image services have 2kB file for speed testing and allow main site
    # with cross origin resource sharing.
    @imageServices = [
      "http://pinkie.mylittlefacewhen.com"
      "http://dashie.mylittlefacewhen.com"
    ]

    @fastest =
      service: undefined
      speed: 10000

    #PING PONG
    _.each @imageServices, (service) =>
      time = new Date().getTime()
      $.ajax
        method: "GET"
        url: service + "/media/speedtest.txt"
        complete: =>
          speed = new Date().getTime() - time
          if speed < @fastest.speed
            @fastest =
              service: service
              speed: speed

    # CSS is stuffed in the main app.js built during deployment
    # TODO: stuff it as <style type='text/css'> into a template instead of js
    # TODO: Think a better way
    #unless debug
    #  $("head").append "<style type='text/css'>" + collated_stylesheets + "</style>"

    # Top bar
    @topView = new TopView().render()

  _trackPageview: ->
    # GoogleAnalytics
    try
      url = Backbone.history.getFragment()
      _gaq.push(['_trackPageview', "/#{url}"])

  getImageService: ->
    # Images may start loading before image service is decided.
    return @fastest.service or @imageServices[0]

  routes:
    "": "new"
    "hot": "hot"
    "new": "new"
    "popular": "popular"
    "unreviewed": "unreviewed"
    "develop": "develop"
    "develop/api": "apidoc"
    "develop/api/:version": "apidoc"
    "changelog": "changes"
    "f": "random"
    "f/:id": "face"
    "face": "random"
    "feedback": "feedback"
    "random": "random"
    "randoms": "randoms"
    "search/*query": "search"
    "submit": "submit"
    "tags": "tags"

  hot: -> @main("-hotness")

  new: -> @main("-id")

  popular: -> @main("-views")

  main: (ordering) ->
    @before "#m_posts", =>
      params =
        collection: @faceList
        order_by: ordering
      return new MainView(params).render()

  unreviewed: ->
    @before "none", =>
      @randFaceList = new FaceCollection()
      return new UnreviewedView(collection: @randFaceList).render()

  apidoc: (version) ->
    @before "#m_api", =>
      version = "v3" if version == null
      console.log version
      return @pageload new APIDocView(version: version)

  changes: ->
    @before "none", => @pageload(new ChangesView())

  develop: ->
    @before "#m_develop", => @pageload(new DevelopView())

  face: (id) ->
    @before "none", =>
      model = @faceList.get(id)
      random = @randFaceList.get(id)
      model = random if random
      unless model
        page = new SingleView({model: new Face({id:id}), firstLoad: @firstLoad})
      else
        page = new SingleView({model:model, firstLoad: @firstLoad})
      return @pageload page

  feedback: ->
    @before "#m_feedback", => @pageload(new FeedbackView())

  random: ->
    if @randomQueue.length < 1
      @randomQueue.fetch
        data:
          order_by: "random"
          limit: 3
          accepted: true
          removed: false
        success: (data) =>
          @random()
    else
      @select("none")
      face = @randomQueue.pop()
      @randFaceList.add face unless @randFaceList.get(face.id)
      app.navigate "f/#{face.get("id")}/", trigger:true

  randoms: ->
    @before "#m_randoms", => new RandomsView().render()

  submit: ->
    @before "#m_submit", => @pageload(new SubmitView())

  search: ->
    @before "none", => new SearchView().render()

  tags: ->
    @before "#m_tags", => @pageload(new TagsView(collection: @tagList))

  pageload: (page) ->
    # Don't redraw the page if it's rendered by the server
    return if @firstLoad then page else page.render()

  select: (item) ->
    # Move the selected menu item indicator
    $("#topmenu div").removeClass("selected")
    $("#{item} div").addClass("selected")

  before: (select, callback) ->
    @select(select)
    @_trackPageview()  # use analytics
    # close old page before opening new one, this takes care of the event listeners.
    @currentPage.close() if @currentPage
    @currentPage = callback()
    # First load is handeled differently due to server generated template
    @firstLoad = false if @firstLoad
    # @topView.updateAd()


# Templates that are loaded during development mode.
# Release version has all of these already loaded in app.js
tpl.loadTemplates [ "main", "thumbnail", "top", "single", "tag", "randoms", "randomsImage", "apidoc-v1", "apidoc-v2", "apidoc-v3", "changelog", "develop", "feedback", "submit", "submitItem", "search", "tags", "tagsItem", "meta"], ->
  # Allow routes with or without trailing slash, just like in Django
  routes = AppRouter::routes
  for route, action of routes
    routes[route + "/"] = action
  AppRouter::routes = routes

  app = new AppRouter()

  Backbone.history.start {pushState: true}
