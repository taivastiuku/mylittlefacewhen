// Generated by CoffeeScript 1.3.1

window.TagsView = Backbone.View.extend({
  el: "#content",
  tags: ["applejack", "fluttershy", "pinkie pie", "rainbow dash", "rarity", "twilight sparkle", "princess celestia", "princess luna", "spike", "derpy hooves", "trixie", "animated", "transparent", "fanart", "screenshot", "untagged", "yes", "do want", "no", "do not want", "creepy", "omg", "lol", "rage", "u mad", "u jelly", "do it filly", "hug"],
  events: {
    "click .thumb a": "navigateAnchor",
    "click #tagcloud a": "navigateAnchor"
  },
  initialize: function() {
    this.template = tpl.get("tags");
    return this.tagsItem_template = tpl.get("tagsItem");
  },
  render: function() {
    var _this = this;
    this.updateMeta();
    if (this.model.models.length === 0) {
      this.model.fetch({
        data:  $.param({
          limit: 10000
        }),
        success: function() {
          return _this.renderIt();
        }
      });
    } else {
      this.renderIt();
    }
    return this;
  },
  renderIt: function() {
    var $tags, data,
      _this = this;
    data = this.model.toJSON();
    $(this.el).html(Mustache.render(this.template, {
      models: data
    }));
    $tags = $("#tags");
    return _.each(this.tags, function(tag) {
      var face, tagsItem;
      tagsItem = $(Mustache.render(_this.tagsItem_template, {
        tag: tag
      }));
      $tags.append(tagsItem);
      face = new FaceCollection();
      return face.fetch({
        data: $.param({
          search: JSON.stringify([tag]),
          order_by: "random",
          limit: 1
        }),
        success: function(data) {
          var imgs, thumb;
          thumb = new Thumbnail({
            model: face.models[0]
          }).render();
          tagsItem.children("div").append(thumb.el.firstChild);
          imgs = $('.lazy');
          if ($.browser.webkit) {
            return imgs.removeClass('lazy').lazyload({
              effect: "fadeIn"
            });
          } else {
            return imgs.removeClass('lazy').lazyload();
          }
        }
      });
    });
  },
  updateMeta: function() {
    $("title").html("Tagcloud and popular tags - MyLittleFaceWhen");
    $("meta[name=description]").attr("content", "All tags known by the service and some of the most frequently needed ones with random pictures.");
    $("#og-image").attr("content", "http://mylittlefacewhen.com/static/cheerilee-square-300.png");
    $("#cd-layout").remove();
    $("link[rel=image_src]").remove();
    return $("link[rel=canonical]").remove();
  }
});

window.TagView = Backbone.View.extend({
  tagName: "span",
  events: {
    "click a": "navigateAnchor"
  },
  initialize: function() {
    return this.template = tpl.get("tag");
  },
  render: function() {
    $(this.el).html(Mustache.render(this.template, {
      name: this.model.get("name")
    }));
    return this;
  }
});
