function TaskListCtrl($scope, $http) {

    $http.get('api/v1.0/queues/automation/status.json').success(function(data) {
        $scope.statuses = data;
    });
    
    $scope.orderProp = 'id';
}
