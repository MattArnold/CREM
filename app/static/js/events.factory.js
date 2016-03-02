angular.module('CREM')
.service('EventsService', ['$http', function ($http) {
  console.log('events service reached');
  var _events = {};

  var _load = $http.get('/eventlist.json');

  _load.success(function(data) {
    _events = data;
    console.log('events list AJAX success', _events);
    return _events;
  }, function(data) {
    console.log('failed to get events list');
    return {error: 'failed to get events list'};
  });

  return {
    events: _events,
    load: _load
  };

}]);
