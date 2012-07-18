app = undefined

# Some views need to clean up before close.
Backbone.View::close = ->
  #console.log "Closing view " + this
  @beforeClose() if @beforeClose
#  @remove()
  @undelegateEvents()


Backbone.View::navigateAnchor = (event) ->
  # Make links work with backbone.js
  event.preventDefault()
  app.navigate(event.currentTarget.getAttribute("href"), {trigger: true})

AppRouter = Backbone.Router.extend
  initialize: ->
    @bind 'all', @_trackPageview
    @faceList = new FaceCollection() #loaded from main view
    @randFaceList = new FaceCollection() #loaded from randoms
    @tagList = new TagCollection()
    if window.location.hash
      @firstLoad = false
    else
      @firstLoad = true

    # Client-side load balancing, list services and pick the fastest one.
    # All image services have 2kB file for speed testing and allow main site
    # with cross origin resource sharing.
    @imageServices = [
      "http://denver.mylittlefacewhen.com"
      "http://scranton.mylittlefacewhen.com"
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
          speed =  new Date().getTime() - time
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
    url = Backbone.history.getFragment()
    _gaq.push(['_trackPageview', "/#{url}"])

  getImageService: ->
    # Images may start loading before image service is decided.
    return @fastest.service if @fastest.service
    return @imageServices[0]

  routes:
    "": "main"
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
    "unreviewed": "unreviewed"


  main: ->
    @before =>
      @select("#m_new")
      return new MainView(model:@faceList).render()

  apidoc: (version) ->
    @before =>
      version = "v2" if version == undefined
      @select("#m_api")
      return @pageload new APIDocView(version: version)

  changes: ->
    @before =>
      @select("none")
      return @pageload new ChangesView()

  develop: ->
    @before =>
      @select("#m_develop")
      return @pageload new DevelopView()
  
  face: (id) ->
    @before =>
      @select("none")
      model = @faceList.get(id)
      r = @randFaceList.get(id)
      model = r if r
      unless model
        page = new SingleView(model: new Face({id:id, not_fetched:true}))
      else
        page = new SingleView(model:model)
      return @pageload page

  feedback: ->
    @before =>
      @select("#m_feedback")
      return @pageload new FeedbackView()

  random: ->
    faces = new FaceCollection()
    faces.fetch
      data:{order_by: "random", limit: 1}
      success: (data) ->
        face = faces.models[0]
        app.faceList.add face unless app.faceList.get(face.id)
        app.navigate("f/" + face.get("id") + "/", {trigger:true})

    @select("none")

  randoms: ->
    @before =>
      @select("#m_randoms")
      return new RandomsView().render()
    
  submit: ->
    @before =>
      @select("#m_submit")
      return @pageload new SubmitView()

  search: ->
    @before =>
      @select("none")
      return new SearchView().render()
  
  tags: ->
    @before =>
      @select("#m_tags")
      return @pageload new TagsView(model:@tagList)

  unreviewed: ->
    @before =>
      @select("none")
      @randFaceList = new FaceCollection()
      return new UnreviewedView(model:@randFaceList).render()

  pageload: (page) ->
    # Don't redraw the page if it's rendered by the server
    # (except for IE9)
    if @firstLoad and not $.browser.msie
      return page
    else
      return page.render()

  select: (item) ->
    # Move the selected menu item indicator
    $("#topmenu div").removeClass("selected")
    $("#{item} div").addClass("selected")

  before: (callback) ->
    # close old page before opening new one, this takes care of the event listeners.
    @currentPage.close() if @currentPage
    @currentPage = callback()
    # First load is handeled differently due to server generated template
    @firstLoad = false if @firstLoad
    @topView.updateAd()

# Templates that are loaded during development mode.
# Release version has all of these already loaded in app.js
tpl.loadTemplates [ "main", "thumbnail", "top", "single", "tag", "randoms", "randomsImage", "apidoc-v1", "apidoc-v2", "changelog", "develop", "feedback", "submit", "submitItem", "search", "tags", "tagsItem", "meta"], ->
  # Allow routes with or without trailing slash, just like in Django
  routes = AppRouter::routes
  for route, action of routes
    routes[route + "/"] = action
  AppRouter::routes = routes

  app = new AppRouter()

  if $.browser.msie and $.browser.version == "9.0" 
    # Internet Explorer lte9 doesn't support pushState history
    Backbone.history.start()
  else
    Backbone.history.start {pushState: true}

