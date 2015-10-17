angular.module('CREM')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
    var responsePromise = $http.get('/tracks.json');

    responsePromise.success(function(data) {
      $scope.tracks = data.tracknames;
    });

    responsePromise.error(function() {
      $scope.tracks = [{ 'name': 'No Tracks Found' }];
    });

  	// TODO: AJAXify this hard-coded data
  	$scope.events = [
  		{
  			title: 'Example Title',
  			room: 'Windover',
  			time: '7 pm',
  			track: 'Tech',
  			presenters: ['Susan Simmons', 'Robert Reed'],
  			description: 'Example of a hard-coded event. This is the description.'
  		},
  		{
  			title: 'Another Example Title',
  			room: 'Charlevoix A',
  			time: '7 pm',
  			track: 'Literature',
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. This is the description of it. These are all grouped by track.'
  		},
  		{
  			title: 'A Food Example Title',
  			room: 'Charlevoix A',
  			time: '7 pm',
  			track: 'Food',
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. This is the description of it.'
  		},
  		{
  			title: 'A Literature Example Title',
  			room: 'Charlevoix A',
  			time: '7 pm',
  			track: 'Literature',
   			presenters: ['Norman Morgenstern', 'Roselyn R. Ferguson'],
 			description: 'Example of another hard-coded event. Grouped by track.'
  		}
   	];
  }
]);
