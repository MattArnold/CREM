angular.module('CREM').controller('AdminController', ['$scope', '$http', function ($scope, $http) {

    var tracksResponsePromise = $http.get('/tracks.json');
    $scope.tracks = {};
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

}])
