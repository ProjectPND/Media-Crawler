(function () {

  'use strict';

  	var app = angular.module('App', ["xeditable"], function($interpolateProvider) {
	    $interpolateProvider.startSymbol('[[');
	    $interpolateProvider.endSymbol(']]');
	});
	
	app.run(['editableOptions', function(editableOptions) {
	  editableOptions.theme = 'default'; // bootstrap3 theme. Can be also 'bs2', 'default'
	}]);

	app.controller('Ctrl', function($scope, $http, $location) {
		var domain = $location.protocol() + "://" + $location.host() + ":" + $location.port();
		// console.log(domain);
		// var data;
		// var self = this;
		// var result = self.result;
		// $scope.result = {}
	  // $scope.user = {
	  //   name: 'awesome user'
	  // };
	  $http({
	      method: 'GET',
	      url: '/api/json'
	   }).then(function success(result){
	   		$scope.media = result.data // This works
	   	// 	$scope.user = {
			  //   name: 'awesome user'
			  // };
	   });
		// console.log($scope.request)

	   // $scope.media = {
	   // 		key : Object.keys($scope.data)
	   // }

	});

}());