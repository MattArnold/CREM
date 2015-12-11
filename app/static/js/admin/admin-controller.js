angular.module('CREM').controller('AdminController', ['$scope', '$http', function ($scope, $http) {

  $scope.convention_name;
  $scope.convention_start_dt = new Date();
  $scope.convention_start_day;
  $scope.convention_end_day;
  $scope.convention_start_time;
  $scope.convention_end_time;
  $scope.timeslot_length;
  var conventionResponsePromise = $http.get('/convention.json');
  conventionResponsePromise.success(function(data) {
    var year, month, day, hours;
    $scope.convention_start_dt = new Date(data.configs[0].start_dt);
    year = $scope.convention_start_dt.getFullYear();
    month = $scope.convention_start_dt.getMonth()+1;
    day = $scope.convention_start_dt.getDate();
    hours = $scope.convention_start_dt.getHours();
    $scope.convention_start_day = year + '-' + month + '-' + day;
    $scope.convention_start_time = hours;
    $scope.convention_name = data.configs[0].name;
    $scope.timeslot_length = data.configs[0].timeslot_length;
  });

  $scope.number_of_timeslots;
  var numberOfTimeslotsResponsePromise = $http.get('/number_of_timeslots.json');
  numberOfTimeslotsResponsePromise.success(function(data) {
    $scope.number_of_timeslots = data.number_of_timeslots;
  });

  $scope.tracks = {};
  $scope.new_track = '';
  var tracksResponsePromise = $http.get('/tracks.json');
  tracksResponsePromise.success(function(data) {
    angular.forEach(data.tracknames, function(track) {
      $scope.tracks[track.uid] = {};
      $scope.tracks[track.uid].uid = track.uid;
      $scope.tracks[track.uid].name = track.name;
      $scope.tracks[track.uid].visible = false;
    });
  });

  $scope.rooms = {};
  $scope.new_room = {};
  var roomsResponsePromise = $http.get('/rooms.json');
  roomsResponsePromise.success(function(data) {
    angular.forEach(data.rooms, function(room) {
      $scope.rooms[room.id] = {};
      $scope.rooms[room.id].id = room.id;
      $scope.rooms[room.id].name = room.name;
      $scope.rooms[room.id].group_id = room.group_id;
      $scope.rooms[room.id].sq_ft = room.sq_ft;
      $scope.rooms[room.id].capacity = room.capacity;
    });
  });

  $scope.room_groups = {};
  $scope.new_room_group = {};
  var roomGroupsResponsePromise = $http.get('/room_groups.json');
  roomGroupsResponsePromise.success(function(data) {
    angular.forEach(data.room_groups, function(room_group) {
      $scope.room_groups[room_group.id] = {};
      $scope.room_groups[room_group.id].id = room_group.id;
      $scope.room_groups[room_group.id].name = room_group.group_name;
    });
  });

}])
