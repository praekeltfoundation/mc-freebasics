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

		// default position and state of the blocks
		blocks: {
			"fb-block-header": { // corresponds with the id of the sortable block
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
	};

	function init() {
		loadConfig();
		initGeneral(site.general);
		initElements();
		initBlocks();
		setGeneralValues();
		arrangeBlocks(site.blocks);
		setStyles();
	}

	// caches jQuery objects based on the names of the styles
	function initElements() {

		that.$siteinput = $('#site-input');
		that.$blockContainer = $('#fb-blockcontainer');
		that.$navBar = $('#steps-container');
		that.$reviewBox = $('#temp-review-box');

		that.$reviewMobi1 = $('#review-mobi-prev-1');
		that.$reviewMobi2 = $('#review-mobi-prev-2');
		that.$reviewMobi3 = $('#review-mobi-prev-3');

		that.$reviewMobi1.slimScroll({height: that.$reviewMobi1.parent().height() });
		that.$reviewMobi2.slimScroll({height: that.$reviewMobi2.parent().height() });
		that.$reviewMobi3.slimScroll({height: that.$reviewMobi3.parent().height() });

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
					saveConfig();
				});
			});
		});

		that.$siteinput.on('keyup', changeSiteName);
		that.$blockContainer.on('changeOrder', changeBlockOrder);
		that.$navBar.on('click', renderReview)
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
		site.general.siteNameUrl = site.general.siteName.replace(/ /g,"-");
		setGeneralValues();
		saveConfig();
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
		saveConfig();
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

	function saveConfig() {
		localStorage.setItem("fb-site", JSON.stringify(getCleansedConfig()));
	}

	function getSavedConfig() {
		return localStorage.getItem("fb-site");
	}

	function deleteSavedConfig() {
		localStorage.removeItem("fb-site");
	}

	function loadConfig() {
		that.siteDefaults = $.extend({}, site);
		var config = getSavedConfig();
		if (config) {
			site = JSON.parse(config);
		} // else default to the pre-existing one
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

	return {
		init: init,
		printConfig: printConfig,
		deleteSavedConfig: deleteSavedConfig
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

fb.init();
