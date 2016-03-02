angular.module('CREM')
.service('ConfigsService', function ($scope, $http) {
  console.log('configsService reached');
  $scope.tracks = {};

  var promise = $http.get('/tracks.json');

  promise.success(function(data) {
    angular.forEach(data.tracknames, function(track) {
      $scope.tracks[track.uid] = {};
      $scope.tracks[track.uid].uid = track.uid;
      $scope.tracks[track.uid].name = track.name;
      $scope.tracks[track.uid].visible = false;
    });
    // TODO: When implementing authentication, set up this line to show the
    // track uid which comes before the @ in the user's penguicon.org email
    // address which is also the user's login id.
    $scope.tracks.tech.visible = true;
  });
  
  promise.error(function() {
    $scope.tracks = [{notracksfound:{'name':'No Tracks Found','uid':'notracksfound',visible:'true'}}];
  });

  return {
    promise: promise
  };
});


