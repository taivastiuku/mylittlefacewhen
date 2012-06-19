window.Face = Backbone.Model.extend
    urlRoot: "/api/v2/face/"

    getImage: ->
        image = undefined
        browser_width = $(window).width()

        if browser_width > @get("width")
            image = @get("image")
        else if browser_width > 1050 and @get("resizes").huge
            image = @get("resizes").huge
        else if browser_width > 700 and @get("resizes").large
            image = @get("resizes").large
        else if browser_width > 400 and @get("resizes").medium
            image = @get("resizes").medium
        else if @get("resizes").small
            image = @get("resizes").small
        else
            image = face.image

        return image


    getThumb: ->
        if @get("thumbnails").gif
            thumb = @get("thumbnails").gif
        else if @get("thumbnails").png
            thumb = @get("thumbnails").png
        else if @get("thumbnails").jpg
            thumb = @get("thumbnails").jpg
        return thumb

window.FaceCollection = Backbone.Collection.extend
    model: Face
    url: "/api/v2/face/"

window.Feedback = Backbone.Model.extend
    urlRoot:"/api/v2/feedback/"

window.Tag = Backbone.Model.extend
    urlRoot: "/api/v2/tag/"

window.TagCollection = Backbone.Collection.extend
    model: Tag
    url: "/api/v2/tag/"
