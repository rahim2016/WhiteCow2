var nav = document.getElementById("navbarSupportedContent");
var btns = nav.getElementsByClassName("nav-link");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}

// // Adding Click event on The signIn Button

/*

var signin = document.getElementById("signin");
if (signin != null) {
    signin.addEventListener("click", (e) => {
        // e.preventDefault();
        if (location.href != 'http://127.0.0.1:8000/login/' && location.href == 'http://127.0.0.1:8000/') {
            location.href = 'login'
        }

        var dropdown = document.getElementById("dropdown");
        dropdown.classList.add("in");

        var dropdownSignUp = document.getElementById("dropdownSignup");
        dropdownSignUp.classList.remove("in");
    })

}



// // Adding Click event on The signUp Button
var signup = document.getElementById("signup");
if (signup != null) {
    signup.addEventListener("click", (e) => {
        // e.preventDefault();

        if (location.href != 'http://127.0.0.1:8000/register/' && location.href == 'http://127.0.0.1:8000/') {
            location.href = 'register'
        }

        var dropdownSignUp = document.getElementById("dropdownSignup");
        dropdownSignUp.classList.add("in");

        var dropdown = document.getElementById("dropdown");
        dropdown.classList.remove("in");
    })
}

*/




// Adding mouseleave event on The Authentication Box
var Authbox = document.getElementById("authbox");
if (Authbox != null) {
    authbox.addEventListener("mouseleave", (e) => {
        var dropdown = document.getElementById("dropdown");
        var dropdownSignUp = document.getElementById("dropdownSignup");
        dropdown.classList.remove("in");
        dropdownSignUp.classList.remove("in");
    })
}

// Add event on Profile User clck 
var userprofile = document.getElementById("Profile");
if (userprofile != null) {
    userprofile.addEventListener("click", (e) => {
        var useraction = document.getElementById("userdropdox");
        useraction.classList.add("in");
    })
}


// Remove event on Profile User clck 
var userprofile = document.getElementById("Profile");
if (userprofile != null) {
    userprofile.addEventListener("mouseleave", (e) => {
        var useraction = document.getElementById("userdropdox");
        useraction.classList.remove("in");
    })
}

var searchcontrol = document.getElementById("searchform");
if (searchcontrol != null) {
    searchcontrol.addEventListener("mouseleave", (e) => {
        var searchbar = document.getElementById("searchtext");
        if (searchbar.value && searchbar) {
            searchcontrol.classList.add("searchbarfocus");
        } else {
            searchcontrol.classList.remove("searchbarfocus");
            searchbar.blur();
        }
    })
}

// // Adding Click event on The searchDeal Button
var searchDealBtn = document.querySelector(".submitButton #btnSub");
var displayblock = document.getElementById("dipblayDealBlock");
var displayform = document.getElementById("dipblayDealBlock");

if (searchDealBtn != null) {

    searchDealBtn.addEventListener("click", (e) => {

        // console.log(searchDealBtn)

    })
}