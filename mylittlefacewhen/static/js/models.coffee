window.Face = Backbone.Model.extend
  urlRoot: "/api/v3/face/"

  getImage: (forced_width) ->
    browser_width = $(window).width()
    browser_width = Math.min(browser_width, forced_width) if forced_width

    resizes = @get("resizes") or {}
    return @get("image") if browser_width > @get("width") and @get("image")
    return resizes.huge if browser_width > 1050 and resizes.huge
    return resizes.large if browser_width > 700 and resizes.large
    return resizes.medium if browser_width > 400 and resizes.medium
    return resizes.small if resizes.small
    return @get("image") or null

  getThumb: (webp, gif) ->
    thumbs = @get("thumbnails") or {}
    return thumbs.gif if thumbs.gif and gif
    return thumbs.png if thumbs.png
    return thumbs.webp if thumbs.webp and webp
    return thumbs.jpg if thumbs.jpg
    return null


window.FaceCollection = Backbone.Collection.extend
  model: Face
  url: "/api/v3/face/"


window.Feedback = Backbone.Model.extend
  urlRoot:"/api/v3/feedback/"


window.Tag = Backbone.Model.extend
  urlRoot: "/api/v3/tag/"


window.TagCollection = Backbone.Collection.extend
  model: Tag
  url: "/api/v3/tag/"


window.Advert = Backbone.Model.extend
  urlRoot: "/api/v3/ad/"


window.AdvertCollection = Backbone.Collection.extend
  model: Tag
  url: "/api/v3/ad/"


window.Comment = Backbone.Model.extend
  urlRoot: "/api/v3/usercomment/"
