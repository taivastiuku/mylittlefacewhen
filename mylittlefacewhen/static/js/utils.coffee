tpl =
  # Hash of preloaded templates for the app
  templates: {}

  # Recursively pre-load all the templates for the app in debug mode
  # or do nothing if in production mode.

  loadTemplates: (names, callback) ->
    unless debug
      callback()
      return

    loadTemplate = (index) =>
      name = names[index]
      $.get static_prefix + "mustache/" + name + ".mustache", (data) =>
        @templates[name] = data
        index++
        if index < names.length
          loadTemplate index
        else
          callback()

    loadTemplate 0

  # Get template by name from hash of preloaded templates
  get: (name) ->
    @templates[name]


atBottom = (offset) ->
    # Is the user at the bottom of the page ?
    offset = 0 unless offset
    return $(document).height() - (window.pageYOffset + window.innerHeight) < offset


getUrlParam = (name) ->
    # Get get-parameter from url.
    # TODO: I think this is part of some utility
    results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href)
    return undefined unless results
    return decodeURI(results[1])


splitter = (urli) ->
    # Get the script part from url.
    # TODO: I think this is part of some utility
    result = urli.split(/com(.+)?/)[1]
    return undefined unless result
    return result
