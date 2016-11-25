// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.is_page_selected = function(page_index) {
      return page_index == self.vue.page_selected;
    };

    //inbox
    function get_solutions_url(status_type, start_idx, end_idx, columnToSort, sortDirection) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx,
            columnToSort: columnToSort,
            sortDirection: sortDirection,
            status_type: status_type
        };
        return solutions_url + "?" + $.param(pp);
    }

    function get_judge_solution_url(status){
        var pp = {
            placeholder: "I'm here because web2py is stupid",
            status: status,
            solution_id: self.vue.solution_reviewing.id
        };
        return judge_solution_url + "?" + $.param(pp);
    }

    //judge solution
    self.judge_solution = function (status) {
        $.getJSON(get_judge_solution_url(status, function(data) {}));
        location.reload();
    };

    //status_type can be either 'pending' or 'judged'
    self.get_solutions = function (status_type) {
        var columnToSort = self.vue.inbox_columns[self.vue.sorting_by].dbName;
        var sortDirection = self.vue.currentSortDirection;
        $.getJSON(get_solutions_url(status_type,0, 5, columnToSort, sortDirection),
          function (data) {
            if (status_type == 'pending') { self.vue.pending_solutions = data.solutions;}
            if (status_type == 'judged') { self.vue.judged_solutions = data.solutions;}
            self.vue.has_more = data.has_more;
          })
    };

    self.beautify_money = function(amount) {
      var unit_symbols = ['', 'K', 'M', 'B','T'];
      if(amount==0) {
        return 0
      }
      else {
        var magnitude =  Math.floor( Math.log(amount) / Math.log(1000) ); //order of magnitude measured in thousands
        var printable_number = amount/(Math.pow(1000,magnitude));
        printable_number = Math.round(printable_number * 1000) / 1000 // rounds to three decimal places
        return printable_number+unit_symbols[magnitude];
      }
    }

    //solution review

    //my problems
    self.get_my_problems = function () {
        $.getJSON(my_problems_url,
          function (data) {
            self.vue.my_problems = data.problems;
            self.vue.has_more = data.has_more;
          })
    };

    //new problem
    self.edit_problem = function(index) {
      self.vue.is_editing_problem = true;
      self.vue.problem_editing = self.vue.my_problems[index];
      self.vue.editing_content.formulation = self.vue.problem_editing.formulation;
      self.vue.editing_content.about = self.vue.problem_editing.about;
      self.vue.editing_content.implications = self.vue.problem_editing.implications;
      self.vue.editing_content.updates = self.vue.problem_editing.updates;

      self.vue.editing_tab = 'formulation'
      self.update_mathjax();
    }
    self.cancel_editing = function() {
      self.vue.is_editing_problem  = false;
    }
    self.update_edit_preview = function() {
      editing_tab = self.vue.editing_tab
      $('.problem-textbox.'+editing_tab).empty();
      $('.problem-textbox.'+editing_tab).text(self.vue.editing_content[editing_tab]);
      self.update_mathjax();
    }
    self.save_problem_edits = function() {
      var new_formulation_content = self.vue.editing_content.formulation;
      var new_about_content = self.vue.editing_content.about;
      var new_implications_content = self.vue.editing_content.implications;
      var new_updates_content = self.vue.editing_content.updates;
      var problem_id = self.vue.problem_editing.id;

      self.vue.problem_editing.formulation = new_formulation_content;
      self.vue.problem_editing.about = new_about_content;
      self.vue.problem_editing.implications = new_implications_content;
      self.vue.problem_editing.updates = new_updates_content;

      $.post(edit_problem_url,
          {
              problem_id: problem_id,
              new_formulation_content: new_formulation_content,
              new_about_content: new_about_content,
              new_implications_content: new_implications_content,
              new_updates_content: new_updates_content
          },
          function (data) {
          }
      )

      self.vue.is_editing_problem  = false;

    };

    //misc
    self.update_mathjax = function() { // this is neccesary because mathjax doesn't reach hidden vue content
      MathJax.Hub.Queue(
      ["Delay", MathJax.Callback, 100],
      ["Typeset", MathJax.Hub]
    );
    }


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
          pages: ['Inbox', 'My Problems', 'New Problem'],
          page_selected: 0, inbox_page: 0, my_problems_page: 1, new_problems_page: 2,

          //inbox variables
          is_reviewing_solution: false,
          solution_reviewing: null,
          inbox_options: ['Pending', 'Completed'],
          inbox_option_selected: 0, inbox_pending_option: 0, inbox_completed_option: 1,
          pending_solutions: [],
          judged_solutions: [],
          has_more: false,
          inbox_columns: [
            {name:'Solution To', dbName:'problem_id'},
            {name:'Submitter', dbName:'attempter_id'},
            {name:'Current Bounty', dbName: null},
            {name: 'Date Submitted', dbName:'date_submitted'},
          ],
          sorting_by: 3, //sets default sorting criteria. Number corresponds to index of columns variable
          currentSortDirection: "HighToLow", //can be "LowToHigh" or "HighToLow"

          //my problems variables
          my_problems: [],
          is_editing_problem: false,
          problem_editing: null,
          editing_tab: 'formulation',
          editing_content:
            {formulation: null, about: 'about poop', implications: 'imp poop', updates: 'up poop'}
        },
        methods: {
            is_page_selected: self.is_page_selected,
            beautify_money: self.beautify_money,

            //my problems methods
            edit_problem: self.edit_problem,
            cancel_editing: self.cancel_editing,
            update_mathjax: self.update_mathjax,
            update_edit_preview: self.update_edit_preview,
            save_problem_edits: self.save_problem_edits,

            //judging
            judge_solution: self.judge_solution
        }

    });

    self.get_solutions('pending');
    self.get_solutions('judged');
    self.get_my_problems();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
