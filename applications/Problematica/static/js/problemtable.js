// This is the js for the default/index.html view.

var app = function(input) {

  //input format:
  //input = {
  //  title: "Some Problems",
  //  initialSize: 5,
  //  incrementSize: 2,
  //  filterType: "ALL", //can be "ALL", "userDonated", "userSolved", or "topic"
  //  filterArguement: null //topic name or userID depending on filtertype
  //}
    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    function get_problems_url(start_idx, end_idx, columnToSort, sortDirection,
      filterType,filterArguement) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx,
            columnToSort: columnToSort,
            sortDirection: sortDirection,
            filterType: filterType,
            filterArguement: filterArguement,
        };
        return problems_url + "?" + $.param(pp);
    }

    self.get_problems = function () {
        var columnToSort = self.vue.columns[self.vue.sorting_by].dbName;
        var sortDirection = self.vue.currentSortDirection;
        var filterType = self.vue.filterType;
        var filterArguement = self.vue.filterArguement;
        $.getJSON(get_problems_url(0, input.initialSize, columnToSort, sortDirection, filterType,
        filterArguement), function (data) {
            self.vue.problems = data.problems;
            self.vue.has_more = data.has_more;
        })
    };

    self.get_more = function () {
        var num_problems = self.vue.problems.length;
        var columnToSort = self.vue.columns[self.vue.sorting_by].dbName;
        var sortDirection = self.vue.currentSortDirection;
        var filterType = self.vue.filterType;
        var filterArguement = self.vue.filterArguement;
        $.getJSON(get_problems_url(num_problems, num_problems + input.incrementSize, columnToSort, sortDirection, filterType,
        filterArguement), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.problems, data.problems);
        });
    };

    self.toggle_sort = function (selectedColumnID) {
        var currentSortDirection = self.vue.currentSortDirection;
        var sorting_by = self.vue.sorting_by;
        if (sorting_by == selectedColumnID) {
          if (currentSortDirection=='HighToLow') {
            self.vue.currentSortDirection = 'LowToHigh';
          }
          else {
            self.vue.currentSortDirection = 'HighToLow';
          }
        }
        else {
          self.vue.sorting_by = selectedColumnID;
          current_bounty = 'LowToHigh';
        }
    }

    self.vue = new Vue({
        el: "#vue-div-"+input.uniqueIdentifier,
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            columns: [
              {name:'title', dbName: 'problem_title'},
              {name:'bounty ($)', dbName: 'current_bounty'},
              {name:'donors', dbName: 'num_donors'},
              {name: 'date posted', dbName: 'date_posted'}
            ],
            sorting_by: 3, //sets default sorting criteria. Number corresponds to index of columns variable
            currentSortDirection: "HighToLow", //can be "LowToHigh" or "HighToLow"
            problems: [],
            has_more: false,
            filterType: input.filterType,      //"ALL", "userSolved", "userDontaed" or "topic"
            filterArguement: input.filterArguement, //by user: user id or topic name depending on filter type
            tableTitle: input.title,
        },
        methods: {
            get_more: self.get_more,
            get_problems: self.get_problems,
            toggle_sort: self.toggle_sort,
        }

    });

    self.get_problems();
    $("#vue-div-"+input.uniqueIdentifier).show();

    return self;
};
