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



    self.donate_button = function () {
        // The button to add a post has been pressed.
        self.vue.is_donating = !self.vue.is_donating;
        console.log('donate button pressed')
    };

    self.add_donation = function () {
        console.log('submit donation button pressed')
        console.log(self.vue.form_post_content)
        // The submit button to add a post has been added.
        //self.vue.form_post_content = "";
        //self.vue.is_adding_post = !self.vue.is_adding_post;
        window.location = donate_button_pressed + '?donation_amount=' + self.vue.form_post_content; //self.vue.form_post_content
    };

    self.go_to_donate_confirmation = function() {
        window.location.href = add_post_url;
    }



    self.vue = new Vue({
        el: "#vue-div1",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_donating: false,
            form_user_email: null,
            form_post_content: null,
            form_edit_post_content: null,
            form_created_on: null,
            form_updated_on: null,
            auth_user: null
        },
        methods: {
            donate_button: self.donate_button,
            add_donation: self.add_donation,
            go_to_donate_confirmation: self.go_to_donate_confirmation,
        }

    });




    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
