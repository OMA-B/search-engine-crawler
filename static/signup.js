import { fetch_users_data } from "./admin.js";
import { check_validity } from "./crawler.js";

// grabbing elements for manipulation
const log_in_page = document.querySelector('.log_in');
const signup_form = document.querySelector('.sign_up form');
const signup_inputs = document.querySelectorAll('.sign_up form input');
const status_message = document.querySelectorAll('.sign_up .status_message');
const login_here = document.querySelector('.login_option button');
const sign_up_page = document.querySelector('.sign_up');
const back_to_admin = document.querySelector('.sign_up .back_to_admin');
const admin_chamber = document.querySelector('.admin_panel_container');

// check if passwords match
const check_passwords = (color, mode) => {
    signup_inputs[2].style.border = `1px solid ${color}`;
    signup_inputs[3].style.border = `1px solid ${color}`;
    status_message[0].hidden = mode;
}

setInterval(() => {
    // scanning inputs for validity
    check_validity(signup_inputs);

    // checking if passwords match
    if (signup_inputs[3].value !== '' && signup_inputs[2].value !== signup_inputs[3].value) {
        check_passwords('red', false)
        status_message[0].textContent = 'Passwords do not match!';
    } else {
        check_passwords('rgb(92, 137, 233)', true)
    }
}, 1000);

// collecting user's data
const save_user_data = async () => {
    if (signup_inputs[2].value === signup_inputs[3].value) {
        const user_data = {
            username: signup_form.username.value,
            email: signup_form.email.value,
            password: signup_form.confirm_password.value,
        };

        // sending user's data to backend
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user_data),
        });
        const data = await response.json();

        if (data.message === 'User created') {
            status_message[1].hidden = false;
            status_message[1].textContent = 'Successfully Registered! Head back to LogIn.'
            fetch_users_data();
        } else {
            status_message[1].hidden = false;
            status_message[1].textContent = data.message;
        }
        setTimeout(() => { status_message[1].hidden = true; }, 10000);
        // clear inputs
        signup_form.reset();
    }
}

// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();

    check_validity(signup_inputs);

    // save user data
    save_user_data();
}

// go to login page if user is not new
const switch_pages = () => {
    log_in_page.hidden = false;
    sign_up_page.hidden = true;
}

// take admin back to admin chamber
const to_admin_chamber = () => {
    sign_up_page.parentElement.hidden = true;
    admin_chamber.hidden = false;
}

// EventListener
signup_form.addEventListener('submit', process_form_data);
login_here.addEventListener('click', switch_pages);
back_to_admin.addEventListener('click', to_admin_chamber);