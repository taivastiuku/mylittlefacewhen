// Generated by CoffeeScript 1.3.3

window.TagsView = Backbone.View.extend({
  el: "#content",
  tags: ["applejack", "fluttershy", "pinkie pie", "rainbow dash", "rarity", "twilight sparkle", "princess celestia", "princess luna", "spike", "derpy hooves", "trixie", "animated", "transparent", "fanart", "screenshot", "untagged", "yes", "do want", "no", "do not want", "creepy", "omg", "lol", "rage", "u mad", "u jelly", "do it filly", "hug"],
  initialize: function() {
    this.title = "Tagcloud and popular tags - MyLittleFaceWhen";
    this.description = "All tags known by the service and some of the most frequently needed ones with random pictures.";
    this.template = tpl.get("tags");
    return this.tagsItem_template = tpl.get("tagsItem");
  },
  events: {
    "click .thumb a": "navigateAnchor",
    "click #tagcloud a": "navigateAnchor"
  },
  render: function() {
    var _this = this;
    this.updateMeta(this.title, this.description);
    if (this.collection.models.length === 0) {
      this.collection.fetch({
        data: {
          limit: 10000
        },
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
    data = this.collection.toJSON();
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
        data: {
          search: JSON.stringify([tag]),
          order_by: "random",
          removed: false,
          accepted: true,
          limit: 1
        },
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
  }
});

window.TagView = Backbone.View.extend({
  tagName: "span",
  initialize: function() {
    return this.template = tpl.get("tag");
  },
  events: {
    "click a": "navigateAnchor"
  },
  render: function() {
    $(this.el).html(Mustache.render(this.template, {
      name: this.collection.get("name")
    }));
    return this;
  }
});
