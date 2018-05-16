/**
 * Angular JavaScript that controls the user interface interactions .
 * @module App module
 * @author Santiago Flores Kanter <sfloresk@cisco.com>
 * @copyright Copyright (c) 2018 Cisco and/or its affiliates.
 * @license Cisco Sample Code License, Version 1.0
 */

/**
 * @license
 * Copyright (c) 2018 Cisco and/or its affiliates.
 *
 * This software is licensed to you under the terms of the Cisco Sample
 * Code License, Version 1.0 (the "License"). You may obtain a copy of the
 * License at
 *
 *                https://developer.cisco.com/docs/licenses
 *
 * All use of the material herein must be in accordance with the terms of
 * the License. All rights not expressly granted by the License are
 * reserved. Unless required by applicable law or agreed to separately in
 * writing, software distributed under the License is distributed on an "AS
 * IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied.
 */

/* Global variables */
TOKEN_TIMEOUT = "Token was invalid (Error: Token timeout)";

var appModule = angular.module('appModule',['ngRoute','ngAnimate'])

/*  Filters    */

// Tells if an object is instance of an array type. Used primary within ng-templates
appModule.filter('isArray', function() {
  return function (input) {
    return angular.isArray(input);
  };
});


// Add new item to list checking first if it has not being loaded and if it is not null.
// Used primary within ng-templates
appModule.filter('append', function() {
  return function (input, item) {
    if (item){
        for (i = 0; i < input.length; i++) {
            if(input[i] === item){
                return input;
            }
        }
        input.push(item);
    }
    return input;
  };
});

// Remove item from list. Used primary within ng-templates
appModule.filter('remove', function() {
  return function (input, item) {
    input.splice(input.indexOf(item),1);
    return input;
  };
});

// Capitalize the first letter of a word
appModule.filter('capitalize', function() {

  return function(token) {
      return token.charAt(0).toUpperCase() + token.slice(1);
   }
});

// Replace any especial character for a space
appModule.filter('removeSpecialCharacters', function() {

  return function(token) {
      return token.replace(/#|_|-|$|!|\*/g,' ').trim();
   }
});

/*  Configuration    */

// Application routing
appModule.config(function($routeProvider, $locationProvider){
    // Maps the URLs to the templates located in the server
    $routeProvider
        .when('/', {templateUrl: 'ng/home'})
        .when('/home', {templateUrl: 'ng/home'})
        .when('/devices', {templateUrl: 'ng/devices'})
        .when('/configuration', {templateUrl: 'ng/configuration'})
        .when('/upgrade', {templateUrl: 'ng/upgrade'})
    $locationProvider.html5Mode(true);
});

// Add to all requests the authorization header
appModule.config(function ($httpProvider){

    $httpProvider.interceptors.push('authInterceptor');
});


appModule.filter('capitalize', function() {
    // Capitalize the first letter of a word
  return function(token) {
      return token.charAt(0).toUpperCase() + token.slice(1);
   }
});

// To avoid conflicts with other template tools such as Jinja2, all between {a a} will be managed by ansible instead of {{ }}
appModule.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

/* Factories */

// The notify factory allows services to notify to an specific controller when they finish operations
appModule.factory('NotifyingService' ,function($rootScope) {
    return {
        subscribe: function(scope, event_name, callback) {
            var handler = $rootScope.$on(event_name, callback);
            scope.$on('$destroy', handler);
        },

        notify: function(event_name) {
            $rootScope.$emit(event_name);
        }
    };
});

// The auth notify factory allows other components subscribe and being notified when authentication is successful
appModule.factory('AuthNotifyingService', function($rootScope) {
    return {
        subscribe: function(scope, callback) {
            var handler = $rootScope.$on('notifying-auth-event', callback);
            scope.$on('$destroy', handler);
        },

        notify: function() {
            $rootScope.$emit('notifying-auth-event');
        }
    };
});

// This factory adds the token to each API request
appModule.factory("authInterceptor", function($rootScope, $q, $window){
    return {
        request: function(config){
            config.headers = config.headers  || {};
            if ($window.sessionStorage.token){
                config.headers.Authorization = 'APIC-TOKEN ' + $window.sessionStorage.token;
            }
            return config;
        },
        responseError: function(rejection){
            if (rejection.status === 401){
                //Manage common 401 actions
            }
            return $q.reject(rejection);
        }
    };
});

/*  Services    */

/* Authentication */
appModule.service("AuthService", function($window, $http, $location, AuthNotifyingService){
    function url_base64_decode(str){
        return window.atob(str)
    }

    this.url_base64_decode = url_base64_decode

    // if token is not stored, try to get it if not in login page
    if ($location.$$path != '/login'){
        if (!$window.sessionStorage.token){
            $http
            .get('api/token')
            .then(function (response, status, headers, config){
                $window.sessionStorage.token = response.data.token;
                AuthNotifyingService.notify();
            })
            .catch(function(response, status, headers, config){
                // Any issue go to login
                $window.location.href = '/login'
            })

        }
    }
})


/*  Controllers    */

appModule.controller('AuthController', function($scope, $http, $window, AuthService, AuthNotifyingService){

    $scope.user = {username: '', password: ''}
    $scope.isAuthenticated = false
    $scope.token = $window.sessionStorage.token;

    $scope.submit = function (){
        $scope.message = "Working...";
        $http
            .post('/api/login/token', $scope.user)
            .then(function (response, status, headers, config){
                $window.sessionStorage.token = response.data.token;
                $scope.token = $window.sessionStorage.token;
                $scope.isAthenticated = true;
                $scope.message = "Success! Loading application";
                $window.location.href = '/web/'
            })
            .catch(function(response, status, headers, config){
                delete $window.sessionStorage.token;
                $scope.isAuthenticated = false;
                $scope.message = response.data;
            })
    }

    $scope.logout = function() {
        $scope.isAuthenticated = false;
        $window.sessionStorage.token = '';
        $window.location.href = '/web/logout'
    }

    AuthNotifyingService.subscribe($scope, function updateToken() {
        $scope.token = $window.sessionStorage.token;
    });
});


// App controller is in charge of managing all services for the application
appModule.controller('AppController', function($scope, $location, $http, $window, $rootScope){

    $scope.loading = false;
    $scope.neighbors = []
    $scope.logged = false;
    $scope.apic = {}
    $scope.logged = false;
    $scope.error = '';
    $scope.success = '';
    $scope.groupAction = 'list';
    $scope.group = {devices: []};
    $scope.groups =[];

    $scope.go = function ( path ) {
        $location.path( path );
    };


    $scope.clearError = function(){
        $scope.error = "";
    };


     $scope.clearSuccess = function(){
        $scope.success = "";
    };


    // Location logic. This tells the controller what to do according the URL that the user currently is
    $scope.$on('$viewContentLoaded', function(event) {
        if (!$scope.logged){
            $scope.go('/');
        }
        if ($location.$$path === '/'){

        }
    });

    $scope.getNeighbors = function(){
        $scope.loading = true;
        $http
            .get('api/neighbors')
            .then(function (response, status, headers, config){

                $scope.neighbors = [];
                if(angular.isArray(response.data)){
                    $scope.neighbors = response.data;
                    for (var i = 0; i < $scope.neighbors.length; i++) {
                        // Change to true if you want the details to be shown by default

                            $scope.neighbors[i].details = false;

                    }
                }
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })

    };

    $scope.login = function(){
        $scope.loading = true;
        $http
            .post('api/login',$scope.apic)
            .then(function (response, status, headers, config){
                $scope.logged = true;
                $scope.getNeighbors();
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
                $scope.loading = false;
            })
            .finally(function(){

            })
    };

    $scope.requestUpgrade = function(item){
        $scope.loading = true;
        $http
            .post('api/upgrade', item)
            .then(function (response, status, headers, config){
                $scope.success="Request sent!"
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                   $scope.loading = false;
            })
    };

    $scope.setGroupAction = function(action){
        $scope.groupAction = action;
    };

    $scope.getGroups = function(){
        $scope.loading = true;
        $http
            .get('api/groups')
            .then(function (response, status, headers, config){
                $scope.groups = response.data;
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })
    };
    $scope.getGroups();

    $scope.addGroup = function(){
        $scope.loading = true;
        $http
            .post('api/groups', $scope.group)
            .then(function (response, status, headers, config){
                $scope.success = "Group created"
                $scope.getGroups();
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })
    };

    $scope.addRemoveDeviceToGroup = function(device){
        var index = $scope.group.devices.indexOf(device);
        if (index > -1) {
          $scope.group.devices.splice(index, 1);
        }
        else{
           $scope.group.devices.push(device)
        }

    };

});
