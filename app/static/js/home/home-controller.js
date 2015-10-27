angular.module('CREM')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
    var columnsResponsePromise = $http.get('/columns.json');
    var tracksResponsePromise = $http.get('/tracks.json');
    $scope.controlsShown = true;
    $scope.tracks = {};
    $scope.allTracksHidden = true;
    $scope.allColumns = [];
    $scope.visibleColumns = [];
    $scope.hiddenColumns = [];
    $scope.orderByColumn = 'track';

    tracksResponsePromise.success(function(data) {
      angular.forEach(data.tracknames, function(track) {
        $scope.tracks[track.uid] = {};
        $scope.tracks[track.uid].uid = track.uid;
        $scope.tracks[track.uid].name = track.name;
      });
    });

    columnsResponsePromise.success(function(data) {
      $scope.allColumns = data.columnnames;
      $scope.visibleColumns = $scope.allColumns;
      // These columns are hidden by default:
      _.each(['eventnumber','type','duration'], function(columnid){
        $scope.hideColumn(columnid);
      });
    });

    function setColumnWidths() {
      // When the screen is at bootstrap's `col-md` width,
      // each event will be two rows. The top row will contain
      // all fields except `description`, adding up to 12
      // bootstrap grid increments. `description` will fill the
      // entire 12 increments of the following row's width.
      var descriptionColumn = _.find($scope.visibleColumns, {'id': 'description'});
      var colsWithoutDesc = _.without($scope.visibleColumns, descriptionColumn);
      var numOfCols = colsWithoutDesc.length;
      var standardWidth = Math.floor(12 / numOfCols);
      // Increase the width of the title if necessary to fill to 12.
      var titleWidth = (standardWidth * (numOfCols - 1)) < 12 ? 12 - (standardWidth * (numOfCols -1)) : standardWidth;
      console.log('numOfCols ' + numOfCols + ' standardWidth ' + standardWidth + ' titleWidth ' + titleWidth);

      _.each($scope.allColumns, function(column){
        column.width = column.id === 'description' ? 12 : standardWidth;
        if (column.id === 'title') {
          column.width = titleWidth;
        }
      });
    }

    $scope.hideColumn = function(columnid) {
      var removedColumn = _.find($scope.visibleColumns, {'id': columnid});
      _.pull($scope.visibleColumns, removedColumn);
      $scope.hiddenColumns.push(removedColumn);
      setColumnWidths();
      // console.log('hiddenColumns ' + JSON.stringify($scope.hiddenColumns));
    }

    $scope.showColumn = function(columnid) {
      var addedColumn = _.find($scope.hiddenColumns, {'id': columnid});
      _.pull($scope.hiddenColumns, addedColumn);
      $scope.visibleColumns.push(addedColumn);
      setColumnWidths();
      // console.log('visibleColumns ' + JSON.stringify($scope.visibleColumns));
    }

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
        day: 'Friday',
        time: '7 pm',
  			track: {uid: 'tech', name: 'Tech'},
  			presenters: ['Susan Simmons', 'Robert Reed'],
  			description: 'Example of a hard-coded event. This is the description.'
  		},
  		{
  			title: 'Another Example Title',
  			room: 'Charlevoix A',
        day: 'Saturday',
  			time: '7 pm',
        track: {uid: 'literature', name: 'Literature'},
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. This is the description of it. These are all grouped by track.'
  		},
  		{
  			title: 'A Food Example Title',
  			room: 'Charlevoix A',
        day: 'Saturday',
  			time: '7 pm',
        track: {uid: 'food', name: 'Food'},
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. This is the description of it.'
  		},
  		{
  			title: 'A Literature Example Title',
  			room: 'Board of Directors',
        day: 'Sunday',
  			time: '7 pm',
        track: {uid: 'literature', name: 'Literature'},
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. Grouped by track.'
  		},
      {
        title: 'A Deployment of Superpages',
        room: 'Charlevoix C',
        day: 'Friday',
        time: '5 pm',
        track: {uid: 'tech', name: 'Tech'},
        presenters: ['Lewis K. Berry'],
      description: 'Cache coherence must work. In fact, few cyberinformaticians would disagree with the analysis of voice-over-IP. AridPrawn, our new application for A* search, is the solution to all of these obstacles.'
      },
      {
        title: 'A Pretend Game',
        room: 'Lobby',
        day: 'Saturday',
        time: '11 am',
        track: {uid: 'gaming', name: 'Gaming'},
        presenters: ['David Ross'],
      description: 'A pretend game as an example event.'
      },
      {
        title: 'E-Commerce Deployment',
        room: 'Board of Governors',
        day: 'Friday',
        time: '9 pm',
        track: {uid: 'tech', name: 'Tech'},
        presenters: ['Paul Burtch'],
      description: 'In recent years, much research has been devoted to the development of Internet QoS; unfortunately, few have harnessed the investigation of systems. Given the current status of amphibious algorithms, hackers worldwide compellingly desire the visualization of XML. DimVendue, our new methodology for scalable configurations, is the solution to all of these obstacles.'
      }
   	];
  }
])
.filter('visibleColumnOrder', function() {
  return function(mysteryVariable, allColumns, visibleColumns, inverted) {
    // console.log('mysteryVariable ' + JSON.stringify(mysteryVariable) + 'allColumns ' + JSON.stringify(allColumns) + ' visibleColumns ' + JSON.stringify(visibleColumns));

    var filtered = _.sortBy(allColumns, visibleColumns);
    // console.log('filtered ' + JSON.stringify(filtered) );
    return filtered;
  };
});
