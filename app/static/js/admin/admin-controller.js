angular.module('CREM').controller('AdminController', ['$scope', '$http', function ($scope, $http) {

    var tracksResponsePromise = $http.get('/tracks.json');
    var roomsResponsePromise = $http.get('/rooms.json');
    var roomGroupsResponsePromise = $http.get('/room_groups.json');
    $scope.tracks = {};
    $scope.rooms = {};
    $scope.room_groups = {};
    $scope.convention_name = '';
    $scope.convention_start_date = new Date();
    $scope.convention_end_date = '';
    $scope.convention_start_time = '';
    $scope.convention_end_time = '';
    $scope.new_track = '';

    tracksResponsePromise.success(function(data) {
      angular.forEach(data.tracknames, function(track) {
        $scope.tracks[track.uid] = {};
        $scope.tracks[track.uid].uid = track.uid;
        $scope.tracks[track.uid].name = track.name;
        $scope.tracks[track.uid].visible = false;
      });
    });

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

    roomGroupsResponsePromise.success(function(data) {
      angular.forEach(data.room_groups, function(room_group) {
        $scope.room_groups[room_group.id] = {};
        $scope.room_groups[room_group.id].id = room_group.id;
        $scope.room_groups[room_group.id].name = room_group.group_name;
      });
    });

}])
