angular.module('CREM')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
    var responsePromise = $http.get('/tracks.json');
    $scope.controlsShown = true;
    $scope.filter = [];

    responsePromise.success(function(data) {
      $scope.tracks = data.tracknames;
    });

    angular.forEach($scope.tracks, function(track) {
      $scope.filter[track.uid] = false;
    });

    $scope.trackFilter = function() {
      var whatwasclicked = this.item.uid;
        console.log('What was clicked was ' + JSON.stringify(whatwasclicked) );
      angular.forEach($scope.tracks, function(track){
        if (track.uid === whatwasclicked){
          if ($scope.filter[whatwasclicked] === true) {
            $scope.filter[whatwasclicked] = false;
          } else {
            $scope.filter[whatwasclicked] = true;
          }
        console.log('track.shown is ' + track.shown);
        }
      });
    };

    responsePromise.error(function() {
      $scope.tracks = [{ 'name': 'No Tracks Found' }];
    });

    $scope.columnnames = [
      {
        id: 'id',
        name: 'ID#'
      },
      {
        id: 'title',
        name: 'Title'
      },
      {
        id: 'track',
        name: 'Track'
      },
      {
        id: 'time',
        name: 'Start'
      },
      {
        id: 'duration',
        name: 'Duration'
      },
      {
        id: 'room',
        name: 'Room'
      },
      {
        id: 'type',
        name: 'Type'
      },
      {
        id: 'presenters',
        name: 'Program Participants'
      },
      {
        id: 'description',
        name: 'Description'
      }
    ];

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
]);
