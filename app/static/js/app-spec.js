describe('CREM Module:', function() {

  var module = angular.module('CREM');

  it("should be registered", function() {
    expect(module).not.toEqual(null);
  });

  describe("Dependencies:", function() {

    deps = module.value('CREM').requires;
    var hasModule = function(m) {
      return deps.indexOf(m) >= 0;
    };

    it("should have angular-toArrayFilter as a dependency", function() {
      expect(hasModule('angular-toArrayFilter')).toBe(true);
    });

  });
});
