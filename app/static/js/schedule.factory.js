(function (app) {
  app.factory("ScheduleFactory", [scheduleFactory]);

  function scheduleFactory() {
    $scope.tracks = {};
    $scope.events = {};
    var tracksResponsePromise = $http.get('/tracks.json');
    var eventsResponsePromise = $http.get('/eventlist.json');
  }

})(angular.module("CREM"));

