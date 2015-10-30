angular.module('CREM')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
    var columnsResponsePromise = $http.get('/columns.json');
    var tracksResponsePromise = $http.get('/tracks.json');
    $scope.controlsShown = true;
    $scope.tracks = {};
    $scope.columns = {};
    $scope.allTracksHidden = false;
    $scope.allColumnsHidden = false;
    $scope.orderByColumn = 'track';

    tracksResponsePromise.success(function(data) {
      angular.forEach(data.tracknames, function(track) {
        $scope.tracks[track.uid] = {};
        $scope.tracks[track.uid].uid = track.uid;
        $scope.tracks[track.uid].name = track.name;
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

      _.each(['eventnumber','title','track','type','start','duration','room','presenters','description'], function(columnid, i){
        $scope.columns[columnid].order = i;
      });
      // These columns are hidden by default:
      _.each(['eventnumber','type','duration'], function(columnid){
        $scope.columns[columnid].visible = false;
      });
      setColumnWidths();
    });

    function setColumnWidths() {
      // When the screen is at bootstrap's `col-md` width,
      // each event will be two rows. The top row will contain
      // all fields except `description`, adding up to 12
      // bootstrap grid increments. `description` will fill the
      // entire 12 increments of the following row's width.
      var colsWithoutDesc = _.clone($scope.columns);
      delete colsWithoutDesc.description;
      var visibleAndHidden = _.countBy(colsWithoutDesc, 'visible');
      var numOfCols = visibleAndHidden[true];
      var standardWidth = Math.floor(12 / numOfCols);
      var accumulatedWidth = standardWidth * numOfCols;

      _.each($scope.columns, function(column){
        column.width = column.id === 'description' ? 12 : standardWidth;
      });

      _.each(['presenters','title','room','start','track','type','duration','eventnumber'], function(columnid){
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
      var visibleTracks;

      $scope.tracks[clicked].visible = $scope.tracks[clicked].visible ? false : true;

      // Test whether all the tracks are now hidden.
      visibleTracks = _.find($scope.tracks, function(track) {
        return track.visible === true;
      });
      $scope.allTracksHidden = visibleTracks ? false : true;
    };

    tracksResponsePromise.error(function() {
      $scope.tracks = [{notracksfound:{'name':'No Tracks Found','uid':'notracksfound',visible:'true'}}];
    });

  	// TODO: AJAXify this hard-coded data
  	$scope.events = [
  		{
  			title: 'Example Title',
  			room: 'Windover',
        start: 'Friday 7 pm',
        trackuid: 'tech',
  			track: 'Tech',
  			presenters: 'Susan Simmons, Robert Reed',
        duration: '1hr',
        type: 'panel',
        eventnumber: 0,
  		description: 'Example of a hard-coded event. This is the description.',
  		},
  		{
  			title: 'Another Example Title',
  			room: 'Charlevoix A',
  			start: 'Saturday 7 pm',
        trackuid: 'literature',
        track: 'Literature',
   			presenters: 'Norman Morgenstern, Roselyn R. Ferguson',
        duration: '2hrs',
        type: 'workshop',
        eventnumber: 1,
 			description: 'Example of another hard-coded event. This is the description of it. These are all grouped by track.'
  		},
  		{
  			title: 'A Food Example Title',
  			room: 'Charlevoix A',
  			start: 'Saturday 7 pm',
        trackuid: 'food',
        track: 'Food',
   			presenters: 'Norman Morgenstern, Roselyn R. Ferguson',
        duration: '1hr',
        type: 'workshop',
        eventnumber: 2,
 			description: 'Example of another hard-coded event. This is the description of it.'
  		},
  		{
  			title: 'A Literature Example Title',
  			room: 'Board of Directors',
  			start: 'Sunday 7 pm',
        trackuid: 'literature',
        track: 'Literature',
   			presenters: 'Norman Morgenstern, Roselyn R. Ferguson',
        duration: '1hr',
        type: 'panel',
        eventnumber: 3,
 			description: 'Example of another hard-coded event. Grouped by track.'
  		},
      {
        title: 'A Deployment of Superpages',
        room: 'Charlevoix C',
        start: 'Friday 5 pm',
        trackuid: 'tech',
        track: 'Tech',
        presenters: 'Lewis K. Berry',
        duration: '1hr',
        type: 'talk',
        eventnumber: 4,
      description: 'Cache coherence must work. In fact, few cyberinformaticians would disagree with the analysis of voice-over-IP. AridPrawn, our new application for A* search, is the solution to all of these obstacles.'
      },
      {
        title: 'A Pretend Game',
        room: 'Lobby',
        start: 'Saturday 11 am',
        trackuid: 'gaming',
        track: 'Gaming',
        presenters: 'David Ross',
        duration: '2hr',
        type: 'game',
        eventnumber: 5,
      description: 'A pretend game as an example event.'
      },
      {
        title: 'E-Commerce Deployment',
        room: 'Board of Governors',
        start: 'Friday 9 pm',
        trackuid: 'tech',
        track: 'Tech',
        presenters: 'Paul Burtch',
        duration: '1hr',
        type: 'talk',
        eventnumber: 6,
      description: 'In recent years, much research has been devoted to the development of Internet QoS; unfortunately, few have harnessed the investigation of systems. Given the current status of amphibious algorithms, hackers worldwide compellingly desire the visualization of XML. DimVendue, our new methodology for scalable configurations, is the solution to all of these obstacles.'
      }
   	];
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
