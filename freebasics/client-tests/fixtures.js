module.exports = function() {
  return {
    fromApi: {
      input: {
        'site_name': "your-site-name",
        'site_name_url': "your-site-name",
        'base_background_color': "#efefef",
        'body_font_family': "\"Open Sans\", Helvetica, sans-serif",
        'block_background_color': "#dfdfdf",
        'block_font_family': "\"Open Sans\", Helvetica, sans-serif",
        'text_transform': "uppercase",
        'accent1': "#69269d",
        'accent2': "#c736c0",
        'header_position': 0,
        'article_position': 1,
        'banner_position': 2,
        'category_position': 3,
        'poll_position': 4,
        'footer_position': 5
      },
      expected: {
        // holds the general config values
        general: {
          siteName: "your-site-name",
          siteNameUrl: "your-site-name"
        },

        // holds the default styles and inputs
        styles: {
          "base-color": {
            "background-color": "#efefef"
          },
          "fb-body": {
            "font-family": "\"Open Sans\", Helvetica, sans-serif"
          },
            "block-heading": {
              "background-color": "#dfdfdf",
              "font-family": "\"Open Sans\", Helvetica, sans-serif",
              "text-transform": "uppercase"
            },
            "fb-accent-1": {
              "color": "#69269d"
            },
              "fb-accent-2": {
                "color": "#c736c0"
              }
        },

          // default position and state of the blocks
        blocks: {
          "fb-block-header": { // corresponds with the id of the sortable block
            position: 0
          },
          "fb-block-article":{
            position: 1
          },
            "fb-block-banner": {
              position: 2
            },
            "fb-block-category": {
              position: 3
            },
              "fb-block-poll": {
                position: 4
              },
              "fb-block-footer": {
                position: 5
              }
        }
      },
    },
    toApi: {
      input: {
        // holds the general config values
        general: {
          siteName: "your-site-name",
          siteNameUrl: "your-site-name"
        },

        // holds the default styles and inputs
        styles: {
          "base-color": {
            "background-color": "#efefef"
          },
          "fb-body": {
            "font-family": "\"Open Sans\", Helvetica, sans-serif"
          },
            "block-heading": {
              "background-color": "#dfdfdf",
              "font-family": "\"Open Sans\", Helvetica, sans-serif",
              "text-transform": "uppercase"
            },
            "fb-accent-1": {
              "color": "#69269d"
            },
              "fb-accent-2": {
                "color": "#c736c0"
              }
        },

          // default position and state of the blocks
        blocks: {
          "fb-block-header": { // corresponds with the id of the sortable block
            position: 0
          },
          "fb-block-article":{
            position: 1
          },
            "fb-block-banner": {
              position: 2
            },
            "fb-block-category": {
              position: 3
            },
              "fb-block-poll": {
                position: 4
              },
              "fb-block-footer": {
                position: 5
              }
        }
      },
      expected: {
        'site_name': "your-site-name",
        'site_name_url': "your-site-name",
        'base_background_color': "#efefef",
        'body_font_family': "\"Open Sans\", Helvetica, sans-serif",
        'block_background_color': "#dfdfdf",
        'block_font_family': "\"Open Sans\", Helvetica, sans-serif",
        'text_transform': "uppercase",
        'accent1': "#69269d",
        'accent2': "#c736c0",
        'header_position': 0,
        'article_position': 1,
        'banner_position': 2,
        'category_position': 3,
        'poll_position': 4,
        'footer_position': 5
      }
    }
	};
};
