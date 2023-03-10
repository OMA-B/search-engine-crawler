import { fetch_csv_file } from "./crawler.js";

// grabbing elements for manipulation
const login_form = document.querySelector('.log_in form');
const login_inputs = document.querySelectorAll('.log_in form input');
const status_message = document.querySelector('.log_in .status_message');
const register_now = document.querySelector('.register_option button');
const log_in_page = document.querySelector('.log_in');
const sign_up_page = document.querySelector('.sign_up');
const user_input_container = document.querySelector('.user_input_container');
const crawling_input_container = document.querySelector('.crawling_input_container');
const admin_panel_container = document.querySelector('.admin_panel_container');
const back_to_admin_containers = document.querySelectorAll('.back_to_admin_container');
const csv_container = document.querySelector('.csv_container');


// scanning inputs for validity
const check_validity = () => {
    login_inputs.forEach(input => {
        if (input.value !== '' && !input.checkValidity()) {
            input.style.border = '1px solid red';
        } else if (input.value !== '' && input.checkValidity()) {
            input.style.border = '1px solid rgb(92, 137, 233)';
        } else {
            input.style.border = '1px solid rgb(92, 137, 233)';
        }
    })
}
setInterval(() => { check_validity() }, 1000);

const show_hide_buttons = (admin_status) => {
    // to display specific buttons for admin and not for other users
    back_to_admin_containers.forEach(button => { admin_status ? button.style.display = 'block' : button.style.display = 'none'; });
    csv_container.hidden = !admin_status
}

// collecting user's data
const confirm_user_data = async () => {
    const user_data = {
        email: login_form.email.value,
        password: login_form.password.value,
    };

    // send user data and wait for a confirmation response
    // console.log(JSON.stringify(user_data));
    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_data),
    });
    const data = await response.json();
    console.log(data);

    // if user data exists, take user to crawler's page
    if (user_data.email === data.email) {
        user_input_container.hidden = true;
        // but if user is admin, redirect to admin chamber instead
        if (data.admin === true) {
            admin_panel_container.hidden = false;
            fetch_csv_file();
        } else {
            crawling_input_container.hidden = false;
        }
        show_hide_buttons(data.admin);
        // clear inputs
        login_form.reset();
    } else {
        status_message.hidden = false;
        status_message.textContent = `${data.message}\nRetry or consider signing up!`;
        setTimeout(() => { status_message.hidden = true; }, 10000);
    }
    // if not, display "incorrect login details" message to user
}

// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();

    // save user data
    confirm_user_data();
}

// go to sign up page if user is new
const switch_pages = () => {
    log_in_page.hidden = true;
    sign_up_page.hidden = false;
}

// EventListener
login_form.addEventListener('submit', process_form_data);
register_now.addEventListener('click', switch_pages);