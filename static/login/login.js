
// add enter key listener
$("#username").keypress(function(event) {
    if (event.keyCode === 13) {
    $("#login").click();
    }
});
$("#password").keypress(function(event) {
    if (event.keyCode === 13) {
    $("#login").click();
    }
});

$("#suser").keypress(function(event) {
    if (event.keyCode === 13) {
    $("#signup").click();
    }
});
$("#spass").keypress(function(event) {
    if (event.keyCode === 13) {
    $("#signup").click();
    }
});

var overlay = document.getElementById("overlay");

// Buttons to 'switch' the page
var openSignUpButton = document.getElementById("slide-left-button");
var openSignInButton = document.getElementById("slide-right-button");

// The sidebars
var leftText = document.getElementById("sign-in");
var rightText = document.getElementById("sign-up");

// The forms
var accountForm = document.getElementById("sign-in-info")
var signinForm = document.getElementById("sign-up-info");

// Open the Sign Up page
openSignUp = () =>{
  // Remove classes so that animations can restart on the next 'switch'
  leftText.classList.remove("overlay-text-left-animation-out");
  overlay.classList.remove("open-sign-in");
  rightText.classList.remove("overlay-text-right-animation");
  // Add classes for animations
  accountForm.className += " form-left-slide-out"
  rightText.className += " overlay-text-right-animation-out";
  overlay.className += " open-sign-up";
  leftText.className += " overlay-text-left-animation";
  // hide the sign up form once it is out of view
  setTimeout(function(){
    accountForm.classList.remove("form-left-slide-in");
    accountForm.style.display = "none";
    accountForm.classList.remove("form-left-slide-out");
  }, 700);
  // display the sign in form once the overlay begins moving right
  setTimeout(function(){
    signinForm.style.display = "flex";
    signinForm.classList += " form-right-slide-in";
  }, 200);
}

// Open the Sign In page
openSignIn = () =>{
  // Remove classes so that animations can restart on the next 'switch'
  leftText.classList.remove("overlay-text-left-animation");
  overlay.classList.remove("open-sign-up");
  rightText.classList.remove("overlay-text-right-animation-out");
  // Add classes for animations
  signinForm.classList += " form-right-slide-out";
  leftText.className += " overlay-text-left-animation-out";
  overlay.className += " open-sign-in";
  rightText.className += " overlay-text-right-animation";
  // hide the sign in form once it is out of view
  setTimeout(function(){
    signinForm.classList.remove("form-right-slide-in")
    signinForm.style.display = "none";
    signinForm.classList.remove("form-right-slide-out")
  },700);
  // display the sign up form once the overlay begins moving left
  setTimeout(function(){
    accountForm.style.display = "flex";
    accountForm.classList += " form-left-slide-in";
  },200);
}

// When a 'switch' button is pressed, switch page
openSignUpButton.addEventListener("click", openSignUp, false);
openSignInButton.addEventListener("click", openSignIn, false);
openSignInButton.click();

var success = document.getElementById("success");
var slabel = document.getElementById("successLabel");
var error = document.getElementById("error");
var elabel = document.getElementById("errorLabel");

function classSwitch(iconId, classContent) {
    document.getElementById(iconId).className = classContent;
}

function restoreBtn(id, icon, iconClass, evnt) {
    var el = document.getElementById(id);
    classSwitch(icon, iconClass);
    el.style.cursor = "pointer";
    el.setAttribute("onclick", evnt);
}

function register() {
    var signup = document.getElementById("signup");
    var sname = document.getElementById("sname");
    var suser = document.getElementById("suser");
    var spass = document.getElementById("spass");
    var signname = sname.value;
    var username = suser.value;
    var password = spass.value;

    classSwitch("sign-up-icon", "fa fa-spinner fa-spin");

    if ( ! /^(.{2,})/.test(signname) ) {
        sname.focus();
        elabel.innerHTML = "請設定 2 個字以上的名稱";
        error.style.display = "block";
        classSwitch("sign-up-icon", "fa fa-pencil-square-o");
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
    } else if ( ! /^(.{8,})/.test(password) ) {
        spass.focus();
        elabel.innerHTML = "請符合指定格的密碼，長度必須為 8 個字元以上";
        error.style.display = "block";
        classSwitch("sign-up-icon", "fa fa-pencil-square-o");
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
    } else if ( ! /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(username) ) {
        suser.focus();
        elabel.innerHTML = "請輸入符合格式的郵箱";
        error.style.display = "block";
        classSwitch("sign-up-icon", "fa fa-pencil-square-o");
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
    } else {
        var encryption = window.btoa(window.btoa(password));
        signup.style.cursor = "not-allowed";
        signup.setAttribute("onclick", "");
        $.ajax({
          type: "POST",
          url: "../user/create",
          data: {
            name: signname,
            email: username,
            password: encryption
          },
          success: function(res){
            slabel.innerHTML = `使用者 ${username} 建立完成`;
            sname.value = "";
            suser.value = "";
            spass.value = "";
            success.style.display = "block";
            openSignInButton.click();
            setTimeout(function() {
              success.style.display = "none";
              setTimeout(function() {
                restoreBtn("signup", "sign-up-icon", "fa fa-pencil-square-o", "register()");
              }, 1000);
            }, 2000);
          },
          error: function(jqXHR, textStatus, errorThrown){
            const statusCode = jqXHR.status;
            if (statusCode == 422){
              elabel.innerHTML = "郵箱地址已被使用";
              suser.focus();
            } else {
              console.log(jqXHR);
              console.log(statusCode);
              elabel.innerHTML = "訪問服務器失敗，請檢查網路是否已連接";
            }
            error.style.display = "block";
            setTimeout(function() {
              error.style.display = "none";
              restoreBtn("signup", "sign-up-icon", "fa fa-pencil-square-o", "register()");
            }, 6000);
          },
        });
    }
}