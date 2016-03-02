angular.module('CREM')
  .controller('HomeController', ['$scope', '$http', 'EventsService', function ($scope, $http, EventsService) {
  console.log('controller reached');

    EventsService
    .load
    .then(function() {
      $scope.events = EventsService.events;
      console.log('after loading ', EventsService.events);
    });
    
    $scope.refresh_events = function() {
      $scope.events = EventsService.events;
      console.log('after refresh ', EventsService.events);
    };
    
    var columnsResponsePromise = $http.get('/columns.json');
    var tracksResponsePromise = $http.get('/tracks.json');
    $scope.controlsShown = true;
    $scope.tracks = {};
    $scope.columns = {};

    $scope.allTracksHidden = false;
    $scope.allTracksShown = false;
    $scope.allColumnsHidden = false;
    $scope.orderByColumn = 'track';

    tracksResponsePromise.success(function(data) {
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

    columnsResponsePromise.success(function(data) {
      $scope.columns = data.columns;
      _.each($scope.columns, function(column){
        column.visible = true;
      });

      _.each(['eventnumber','title','track','type','start','duration','room','presenters','resources','description','comments'], function(columnid, i){
        $scope.columns[columnid].order = i;
      });
      // These columns are hidden by default:
      _.each(['eventnumber','type','resources','duration','comments'], function(columnid){
        $scope.columns[columnid].visible = false;
      });
      setColumnWidths();
    });

    function setColumnWidths() {
      // When the screen is at bootstrap's `col-md` width, each event will be
      // multiple rows. The top row will contain all fields except
      // `description` and `comments`, adding up to 12 bootstrap grid
      // increments. `description` and `comments` will each fill the entire 12
      // increments of its row's width.
      var colsWithoutLong = _.clone($scope.columns);
      delete colsWithoutLong.description;
      delete colsWithoutLong.comments;
      var visibleAndHidden = _.countBy(colsWithoutLong, 'visible');
      var numOfCols = visibleAndHidden[true];
      var standardWidth = Math.floor(12 / numOfCols);
      var accumulatedWidth = standardWidth * numOfCols;

      _.each($scope.columns, function(column){
        column.width = standardWidth;
      });

      $scope.columns.description.width = 12;
      $scope.columns.comments.width = 12;

      _.each(['presenters','title','resources','room','start','track','type','duration','eventnumber'], function(columnid){
        if (accumulatedWidth < 12 && $scope.columns[columnid].visible) {
          $scope.columns[columnid].width++;
          accumulatedWidth++;
        }
      });
    }

    $scope.columnFilter = function() {
      var clicked = this.column.id;
      var columnsMadeVisible;

      $scope.columns[clicked].visible = $scope.columns[clicked].visible ? false : true;

      // Test whether all the columns are now hidden.
      columnsMadeVisible = _.find($scope.columns, function(column) {
        return column.visible === true;
      });
      $scope.allColumnsHidden = columnsMadeVisible ? false : true;
      setColumnWidths();
    };

    $scope.trackFilter = function() {
      // "this" refers to the filter button HTML element.
      // ng-repeat attaches data to it. Angular reserves the word
      // 'track' in templates as a verb, so I apologize for
      // replacing it with the vague word 'item'.
      var clicked = this.item.uid;

      $scope.tracks[clicked].visible = $scope.tracks[clicked].visible ? false : true;

      checkTrackVisibility();
    };

    // Either turn all tracks on, or all tracks off.
    $scope.hideOrShowAllTracks = function() {

      if ($scope.allTracksShown) {
        _.each($scope.tracks, function(track){
          track.visible = false;
        });
      } else {
        _.each($scope.tracks, function(track){
          track.visible = true;
        });
      }

      checkTrackVisibility();
    };

    function checkTrackVisibility() {
      $scope.allTracksHidden = _.every($scope.tracks, {'visible':false});
      $scope.allTracksShown  = _.every($scope.tracks, {'visible':true});
    };

    tracksResponsePromise.error(function() {
      $scope.tracks = [{notracksfound:{'name':'No Tracks Found','uid':'notracksfound',visible:'true'}}];
    });

  }
]).directive("contenteditable", function() {
  return {
    restrict: "A",
    require: "ngModel",
    link: function(scope, element, attrs, ngModel) {

      function read() {
        ngModel.$setViewValue(element.html());
      }

      ngModel.$render = function() {
        element.html(ngModel.$viewValue || "");
      };

      element.bind("blur keyup change", function(a) {
        scope.$apply(read);
        element[0].classList.remove('odd', 'even', 'unedited');
        element[0].classList.add('alert-warning', 'edited');
      });
    }
  };
});
