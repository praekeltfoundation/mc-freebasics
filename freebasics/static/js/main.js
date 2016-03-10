var fb = (function($) {
	var that = this;

	var site = {

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
				position: 2
			},
			"fb-block-banner": {
				position: 1
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
	};

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function setupCsrf(){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                var csrftoken = getCookie('csrftoken');
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }

	function init(conf) {
		that.serverUrl = conf.template_data_url;
		that.isNew = conf.isNew;
		that.useLocalStorage = false;
    setupCsrf()

		// TODO: stick this in a pre-init block along with other non-dependents
        that.$notificationBell = $('#notification-bell');

    // use a promise to only continue initialisation when config load complete
    $.when( loadConfig() )
        .then( setupConfig )
        .fail( function(data, textStatus, jqXHR) {
            ajaxErrorLoad(data, textStatus, jqXHR);
            setupConfig();
        });
	}

	// continue with the rest of initialisation once the config has been loaded
	function initContinued() {
		initGeneral(site.general);
		initElements();
		initBlocks();
		setGeneralValues();
		arrangeBlocks(site.blocks);
		setStyles();
        postInit();
	}

	// callback after sync or async config loaded. If it's async, data will be populated with JSONP callback data
	function setupConfig(data, textStatus, jqXHR) {
		if (data && data.length > 0) {
			that.loadedConfig = data;
		}
        if (!that.loadedConfig) {
            // fall back to defaults
            that.loadedConfig = that.siteDefaults;
        }
		site = that.loadedConfig;
		initContinued();
	}

	// caches jQuery objects based on the names of the styles
	function initElements() {

		that.$siteinput = $('#site-input');
		that.$blockContainer = $('#fb-blockcontainer');
		that.$renderReview = $('.render-review');
		that.$reviewBox = $('#temp-review-box');
		that.$buttonDone = $('#button-done');

		that.$reviewMobi1 = $('#review-mobi-prev-1');
		that.$reviewMobi2 = $('#review-mobi-prev-2');
		that.$reviewMobi3 = $('#review-mobi-prev-3');

		that.$reviewMobi1.slimScroll({height: that.$reviewMobi1.parent().height() });
		that.$reviewMobi2.slimScroll({height: that.$reviewMobi2.parent().height() });
		that.$reviewMobi3.slimScroll({height: that.$reviewMobi3.parent().height() });

		that.$printsiteWrapper = $('#printsite-wrapper');
        that.$printsite = $('#printsite');
		that.$printsitelabel1 = $('#printsitelabel1');
		that.$printsitelabel2 = $('#printsitelabel2');

		that.$inputs = {};
		_.each(_.keys(site.styles), function(classKey) {
			var cssClass = site.styles[classKey];

			_.each(_.keys(cssClass), function(styleKey) {
				var styleValue = cssClass[styleKey];
				var inputName = getUniqueStyleName(classKey, styleKey);
				var input = that.$inputs[inputName] = $('#' + inputName);
				input.val(styleValue);
				input.bind('change', function(event) {
					var styleValueInput = input.val();
					site.styles[classKey][styleKey] = styleValueInput;
					setStyle(classKey, styleKey, styleValueInput);
				});
			});
		});

		that.$siteinput.on('keyup', changeSiteName);
		that.$blockContainer.on('changeOrder', changeBlockOrder);
		that.$renderReview.on('click', renderReview);
        that.$buttonDone.on('click', saveConfig );

        $("input.color-picker").each(function () {
            var $el = $(this);
            $el.ColorPickerSliders({
                size: 'sm',
                placement: 'bottom',
                swatches: false,
                sliders: false,
                hsvpanel: true,
                onchange: function () {
                    $el.trigger('change');
                }
            });
        });

        $("#fb-blockcontainer").sortable({
            items: "li.fb-block:not(.locked-sect)",
            placeholder: "sort-highlight",
            handle: ".handle",
            forcePlaceholderSize: true,
            axis: 'y',
            grid: [ 200, 1 ],
            scroll: true,
            scrollSensitivity: 100,
            //tolerance: "pointer",
            zIndex: 999999,
            change: function (event, ui) {
                $(event.target).trigger('changeOrder');
            }
        });
    }

    function postInit() {
        $(".fade").removeClass("out");
    }

	function getUniqueStyleName(cssClass, styleName) {
		return cssClass + "_" + styleName;
	}

	// dynamically creates or rewrites a css style
	function setStyle(cssClass, styleName, styleValue) {
		var uniqueStyleName = getUniqueStyleName(cssClass, styleName);
		var styleId = 'dynamic-style-' + uniqueStyleName;
		var $existingStyle = $('#' + styleId);
		if ($existingStyle.length === 0) {
			$existingStyle = $('<style type="text/css" id="' + styleId + '"></style>');
			$existingStyle.appendTo('head');
		}

		var styleText;
		if (cssClass == 'fb-body') {
			styleText = '.' + cssClass + ', .' + cssClass + ' *:not(.no-' + cssClass + ') {' + styleName + ':' + styleValue + '}';
		} else {
			styleText = '.fb-body .' + cssClass + ' {' + styleName + ':' + styleValue + '}';
		}

		$existingStyle.html(styleText);
	}

	// sets all the current styles
	function setStyles() {
		_.each(_.keys(site.styles), function(classKey) {
			var cssClass = site.styles[classKey];
			_.each(_.keys(cssClass), function(styleKey) {
				setStyle(classKey, styleKey, cssClass[styleKey]);
			});
		});
	}

	function initGeneral(config) {
		site.general = _.extend( site.general, config);
	}

	function setGeneralValues() {
		if (site.general.siteNameUrl !== that.siteDefaults.general.siteNameUrl) {
			that.$siteinput.val(site.general.siteName);
		}
		that.$printsite.html(site.general.siteNameUrl);
		that.$printsitelabel1.html(site.general.siteName);
		that.$printsitelabel2.html(site.general.siteName);
	}

	function changeSiteName() {
		site.general.siteName = that.$siteinput.val();
		site.general.siteNameUrl = site.general.siteName.replace(/ /g,"-").toLowerCase();
		setGeneralValues();
	}

	function changeBlockOrder() {
		var $blocks = that.$blockContainer.children('.fb-block');
		$blocks = _.sortBy( $blocks, function(block) {
			return $(block).position().top
		});
		var position = 0;
		_.each( $blocks, function(block) {
			var blockName = $(block).attr('id');
			site.blocks[blockName].position = position++;
		});
	}

	// block handling
	function initBlocks() {
		// cache all $els
		_.each(_.keys(site.blocks), function(blockName) {
			var block = site.blocks[blockName];
			block.$el = $('#' + blockName);
		});
	}

	// block handling
	function arrangeBlocks(config) {

		// overwrite the existing ordering
		_.each(_.keys(config), function(blockName) {
			site.blocks[blockName].position = config[blockName].position;
		});

		var sortedBlocks = _.sortBy(_.values(site.blocks), function(block) {
			return -block.position;
		});

		_.each(sortedBlocks, function(block) {
			that.$blockContainer.prepend(block.$el.detach())
		});
	}

	// debug info - print the current config state
	function printConfig() {
		console.log( JSON.stringify(getCleansedConfig(), null, 2 ) );
	}

	// return a copy of the config without $els
	function getCleansedConfig() {
		var clonedSite = $.extend(true, {}, site);
		recurse(clonedSite, deleteBlacklistedProperties);
		return clonedSite;
	}

	function recurse(obj, callback) {
		for (var property in obj) {
			if (obj.hasOwnProperty(property)) {
				if (typeof obj[property] == "object") {
					recurse(obj[property], callback);
				} else {
					callback(obj, property)
				}
			}
		}
	}

	function saveConfigLocalStorage() {
		localStorage.setItem("fb-site", JSON.stringify(getCleansedConfig()));
	}

	function getSavedConfigLocalStorage() {
		return localStorage.getItem("fb-site");
	}

	function deleteSavedConfigLocalStorage() {
		localStorage.removeItem("fb-site");
	}

	function saveConfig() {
		$.when( saveConfigPromise() ).then( saveConfigCallback );
	}

	function saveConfigPromise() {
		if (that.useLocalStorage) {
			saveConfigLocalStorage();
			return true;
		} else {
			return saveConfigAjax();
			$.when( saveConfigAjax() ).then( setupConfig );
		}
	}

	function saveConfigCallback(data, textStatus, jqXHR) {
        window.location.href = '/';
	}

	function loadConfig() {
		that.siteDefaults = $.extend({}, site);
		if (that.useLocalStorage) {
			that.loadedConfig = JSON.parse(getSavedConfigLocalStorage());
			return true;
		}
		else if (that.isNew) {
		 return _.clone(that.siteDefaults);
	 }
		else {
			return loadConfigAjax();
		}
	}

	function deleteBlacklistedProperties(obj, key) {
		delete obj.$el;
	}

	function getSortedBlocks() {
		return _.sortBy(_.values( site.blocks ), function(block) {
			return block.position;
		});
	}

	function renderReview() {
		that.$reviewBox.empty();
		that.$reviewMobi1.empty();
		that.$reviewMobi2.empty();
		that.$reviewMobi3.empty();
		_.each( getSortedBlocks(), function(block) {
			var $block = block.$el.find('.grab-sect');
			that.$reviewBox.append( $block.clone() );
			that.$reviewMobi1.append( $block.clone() );
			that.$reviewMobi2.append( $block.clone() );
			that.$reviewMobi3.append( $block.clone() );
		});
	}

    //TODO: Handle errors a lot better and more gracefully. No alerts
	function ajaxErrorLoad(data, textStatus, jqXHR) {
		var msg = "Could not retrieve config using Ajax call. Reverting to default config.";
        that.$notificationBell.append('<span title="' + msg + '" class="label label-danger">!</span>');
        console.log(msg);
        // this is clumsy, but I want to avoid any misunderstanding - for dev work only
        $('#global-options-header').html("Global Options: FROM DEFAULT VALUES");
    }

    function ajaxErrorSave(data, textStatus, jqXHR) {
        var msg = "Could not save config using Ajax call";
        console.log(msg);
        that.$notificationBell.append('<span title="' + msg + '" class="label label-danger">!</span>');
    }

	function loadConfigAjax() {
		return $.ajax({url: that.serverUrl}).then(fromApi);
	}

	function saveConfigAjax() {
		return $.ajax({
			url: that.serverUrl,
			type: that.isNew
  			? 'POST'
  			: 'PUT',
			dataType: 'json',
			data: JSON.stringify(toApi(site))
		});
	}

        function fromApi(d) {
					return {
						general: {
							siteName: d.site_name,
							siteNameUrl: d.site_name_url
						},
						styles: {
							"base-color": {
								"background-color": d.base_background_color
							},
							"fb-body": {
								"font-family": d.body_font_family
							},
							"block-heading": {
								"background-color": d.block_background_color,
								"font-family": d.block_font_family,
								"text-transform": d.text_transform
							},
							"fb-accent-1": {
								"color": d.accent1
							},
							"fb-accent-2": {
								"color": d.accent2
							}
						},

						// default position and state of the blocks
						blocks: {
							"fb-block-header": { // corresponds with the id of the sortable block
								position: d.header_position
							},
							"fb-block-article":{
								position: d.article_position
							},
							"fb-block-banner": {
								position: d.banner_position
							},
							"fb-block-category": {
								position: d.category_position
							},
							"fb-block-poll": {
								position: d.poll_position
							},
							"fb-block-footer": {
								position: d.footer_position
							}
						}
					};
        }

        function toApi(d) {
            return {
							'site_name': d.general.siteName,
							'site_name_url': d.general.siteNameUrl,
							'base_background_color': d.styles["base-color"]["background-color"],
				      'body_font_family': d.styles["fb-body"]["font-family"],
							'block_background_color': d.styles["block-heading"]["background-color"],
				      'block_font_family': d.styles["block-heading"]["font-family"],
							'text_transform': d.styles["block-heading"]["text-transform"],
							'accent1': d.styles["fb-accent-1"].color,
							'accent2': d.styles["fb-accent-2"].color,
				      'header_position': d.blocks["fb-block-header"].position,
							'article_position': d.blocks["fb-block-article"].position,
							'banner_position': d.blocks["fb-block-banner"].position,
				      'category_position': d.blocks["fb-block-category"].position,
							'poll_position': d.blocks["fb-block-poll"].position,
							'footer_position': d.blocks["fb-block-footer"].position
						};
        }

	return {
                fromApi: fromApi,
                toApi: toApi,
		init: init,
		printConfig: printConfig,
		deleteSavedConfig: deleteSavedConfigLocalStorage
	};
})(jQuery);

/*var config = {
	general: {
		siteName: "your-site-name",
		siteNameUrl: "your-site-name"
	},
	styles: {
		"fb-body": {
			"background-color": "#ffffff",
			"color": "#000000",
			"font-family": "Arial, Helvetica, sans-serif"
		},
		"fb-accent-1": {
			"color": "#4383CD"
		},
		"fb-accent-2": {
			"color": "#97ee7b"
		}
	},
	blocks: {
		"fb-block-header": {     // corresponds with the id of the sortable block
			position: 0
		},
		"fb-block-article":{
			position: 4
		},
		"fb-block-banner": {
			position: 2
		},
		"fb-block-category": {
			position: 3
		},
		"fb-block-poll": {
			position: 1
		},
		"fb-block-footer": {
			position: 5
		}
	}
};*/

if (typeof exports === 'object' && typeof module === 'object') {
    module.exports = fb;
}
