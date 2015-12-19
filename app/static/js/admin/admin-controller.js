angular.module('CREM').controller('AdminController', ['$scope', '$http', 'localStorageService', function ($scope, $http, localStorageService) {

  $scope.new_track = '';
  $scope.new_room = {};
  $scope.new_room_group = {};

  // Whenever the config data in Angular changes, immediately save
  // it to the browser's local storage.
  $scope.$watch('configs', function() {
    localStorageService.set('configs', $scope.configs);
  }, true);

  // Load the configs from the browser's local storage.
  var storedConfigs = localStorageService.get('configs');
  $scope.configs = storedConfigs || undefined;

  // Check to make sure nothing is missing from local storage,
  // just in case an AJAX call is necessary after all.
  if ($scope.configs) {

    var configsChecklist = [
      'start_dt',
      'start_day',
      'start_time',
      'name',
      'timeslot_length',
      'number_of_timeslots',
      'rooms',
      'room_groups',
      'tracks'
    ];

    var allConfigsExist = true;

    angular.forEach(configsChecklist, function(config){
      if (!$scope.configs[config]){
        allConfigsExist = false;
      }
    });
  }

  // If there is no local storage, or if any configs are missing
  // in local storage, make an AJAX call to get it from the db.
  if (!allConfigsExist) {

    console.log('AJAX');

    var conResponsePromise = $http.get('/configs.json');

    conResponsePromise.success(function(data) {
      $scope.configs = {};

      $scope.configs.start_dt = new Date(data.convention.start_dt);
      var year, month, day, hours;
      year = $scope.configs.start_dt.getFullYear();
      month = $scope.configs.start_dt.getMonth()+1;
      day = $scope.configs.start_dt.getDate();
      hours = $scope.configs.start_dt.getHours();
      $scope.configs.start_day = year + '-' + month + '-' + day;
      $scope.configs.start_time = hours;
      $scope.configs.name = data.convention.name;
      $scope.configs.timeslot_length = data.convention.timeslot_length;
      $scope.configs.number_of_timeslots = data.convention.number_of_timeslots;
      $scope.calculateEnd();

      $scope.configs.rooms = {};
      angular.forEach(data.rooms, function(room) {
        $scope.configs.rooms[room.id] = {};
        $scope.configs.rooms[room.id].id = room.id;
        $scope.configs.rooms[room.id].name = room.name;
        $scope.configs.rooms[room.id].group_id = room.group_id;
        $scope.configs.rooms[room.id].sq_ft = room.sq_ft;
        $scope.configs.rooms[room.id].capacity = room.capacity;
      });

      $scope.configs.room_groups = {};
      angular.forEach(data.room_groups, function(room_group) {
        $scope.configs.room_groups[room_group.id] = {};
        $scope.configs.room_groups[room_group.id].id = room_group.id;
        $scope.configs.room_groups[room_group.id].name = room_group.group_name;
      });

      $scope.configs.tracks = {};
      angular.forEach(data.tracks, function(track) {
        $scope.configs.tracks[track.uid] = {};
        $scope.configs.tracks[track.uid].uid = track.uid;
        $scope.configs.tracks[track.uid].name = track.name;
        $scope.configs.tracks[track.uid].visible = false;
      });

    });

  }

  $scope.calculateEnd = function() {
    var new_start_dt = new Date($scope.configs.start_day);
    new_start_dt.setHours($scope.configs.start_time);
    var duration = $scope.configs.timeslot_length * $scope.configs.number_of_timeslots;
    var end_dt = new Date(new_start_dt.getTime() + duration * 60000);
    var year, month, day, hours, meridiem;
    year = end_dt.getFullYear();
    month = end_dt.getMonth()+1;

    day = end_dt.getDate();
    $scope.configs.end_day = month + '/' + day + ', ' + year;

    hours = end_dt.getHours();
    meridiem = " AM";
    if (hours >= 12) {
      hours = hours - 12;
      meridiem = " PM";
    }
    if (hours === 0) {
      hours = 12;
    }
    $scope.configs.end_time = hours + meridiem;
    var newyear, newmonth, newday, newhours;
    newyear = new_start_dt.getFullYear();
    newmonth = new_start_dt.getMonth()+1;
    newday = new_start_dt.getDate();
    newhours = new_start_dt.getHours();
    $scope.configs.start_dt = newyear + '-' + newmonth + '-' + newday + 'T:' + newhours;
  }

  $scope.saveConfigsToDB = function() {
    var req = {
      method: 'POST',
      url: '/convention.json',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
          'name': $scope.configs.name,
          'start_dt': $scope.configs.start_dt,
          'timeslot_length': $scope.configs.timeslot_length,
        }
    }

    $http(req).then(function(){
      console.log('success', req);
    }, function(){
      console.log('failure', req);
    });
  }

}])
