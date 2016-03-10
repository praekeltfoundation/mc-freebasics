// fake things main.js expects it
global.jQuery = {};
var assert = require('assert');
var fb = require('../static/js/main');
var fixtures = require('./fixtures');


describe("fb", function() {
  describe("toApi", function() {
    it("should parse data from the api to what the client is expecting",
    function() {
      var d = fixtures().fromApi;
      assert.deepEqual(fb.fromApi(d.input), d.expected);
    });
  });

  describe("fromApi", function() {
    it("should parse data from the client to what the api is expecting",
    function() {
      var d = fixtures().toApi;
      assert.deepEqual(fb.toApi(d.input), d.expected);
    });
  });
});
