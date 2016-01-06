angular.module('CREM').controller('AdminController', ['$scope', '$http', 'localStorageService', function ($scope, $http, localStorageService) {

  $scope.new_track = '';
  $scope.new_room = {};
  $scope.new_room.name = '';
  $scope.new_room.sq_ft = 0;
  $scope.new_room.group_id = '';
  $scope.new_room.capacity = 0;

  $scope.new_room_group = '';

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

      $scope.configs.rooms = [];
      angular.forEach(data.rooms, function(room) {
        if (room.group_id) {
          room.group_id--;
        };
        appendRoom(room);
      });

      $scope.configs.room_groups = data.room_groups;

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

  function appendRoom(room) {
    var appended_room = {};
    appended_room.id = room.id;
    appended_room.name = room.name;
    appended_room.group_id = room.group_id;
    appended_room.sq_ft = room.sq_ft;
    appended_room.capacity = room.capacity;
    $scope.configs.rooms.push(appended_room);
  };

  $scope.createNewRoom = function() {
    if (!_.includes($scope.configs.rooms, $scope.new_room) ){
      $scope.new_room.group_id = $scope.new_room.group_id;
      appendRoom($scope.new_room);
      $scope.new_room = {};
    }
  }

  $scope.createNewRoomGroup = function() {
    // Make sure it is not already in room_groups
    if (!_.includes($scope.configs.room_groups, $scope.new_room_group) ){
      $scope.configs.room_groups.push($scope.new_room_group);
      $scope.new_room_group = '';
    }
  }

  $scope.saveConfigsToDB = function() {

    var conventionreq = {
      method: 'POST',
      url: '/convention.json',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
          'name': $scope.configs.name,
          'start_dt': $scope.configs.start_dt,
          'timeslot_length': $scope.configs.timeslot_length,
          'number_of_timeslots': $scope.configs.number_of_timeslots,
        }
    }
    var roomsreq = {
      method: 'POST',
      url: '/rooms.json',
      headers: {
        'Content-Type': 'application/json'
      },
      data: $scope.configs.rooms,
    }

    $http(roomsreq).then(function(){
      console.log('roomsreq success', roomsreq);
    }, function(){
      console.log('roomsreq failure', roomsreq);
    });

    $http(conventionreq).then(function(){
      console.log('conventionreq success', conventionreq);
    }, function(){
      console.log('conventionreq failure', conventionreq);
    });
  }

}])
