(function (app) {
  app.factory("UiService", ['$scope', '$http', _uiService]);

  function _uiService($scope, $http) {
    $scope.controlsShown = true;

    $scope.columnsResponsePromise = $http.get('/columns.json');

    $scope.columns = {};

    columnsResponsePromise.success(function(data) {
      $scope.columns = data.columns;
      _.each($scope.columns, function(column){
        column.visible = true;
      });

    });

  }

})(angular.module('CREM'));
