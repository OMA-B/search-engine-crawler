// grabbing elements for manipulation
const login_form = document.querySelector('.log_in form');
const login_inputs = document.querySelectorAll('.log_in form input');
const status_message = document.querySelector('.log_in .status_message');
const register_now = document.querySelector('.register_option button');
const log_in_page = document.querySelector('.log_in');
const sign_up_page = document.querySelector('.sign_up');
const user_input_container = document.querySelector('.user_input_container');
const crawling_input_container = document.querySelector('.crawling_input_container');

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

// collecting user's data
const confirm_user_data = async () => {
    const user_data = {
        email: login_form.email.value,
        password: login_form.password.value,
    };

    // send user data and wait for a confirmation response
    console.log(JSON.stringify(user_data));
    // const response = await fetch('http://127.0.0.1:5500/login', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(user_data),
    // });
    // const data = await response.JSON();
    // console.log(data);

    // if user data exists, take user to crawler's page
    user_input_container.hidden = true;
    crawling_input_container.hidden = false;
    // if not, display "incorrect login details" message to user
}

// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();

    // save user data
    confirm_user_data();

    // clear inputs
    login_form.reset()
}

// go to sign up page if user is new
const switch_pages = () => {
    log_in_page.hidden = true;
    sign_up_page.hidden = false;
}

// EventListener
login_form.addEventListener('submit', process_form_data);
register_now.addEventListener('click', switch_pages)