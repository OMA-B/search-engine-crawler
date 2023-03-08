// grabbing elements for manipulation
const log_in_page = document.querySelector('.log_in');
const signup_form = document.querySelector('.sign_up form');
const signup_inputs = document.querySelectorAll('.sign_up form input');
const status_message = document.querySelector('.sign_up .status_message');
const login_here = document.querySelector('.login_option button');
const sign_up_page = document.querySelector('.sign_up');
const back_to_admin = document.querySelector('.sign_up .back_to_admin');
const admin_chamber = document.querySelector('.admin_panel_container');

// scanning inputs for validity
const check_validity = () => {
    signup_inputs.forEach(input => {
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
const save_user_data = async () => {
    const user_data = {
        username: signup_form.username.value,
        email: signup_form.email.value,
        password: signup_form.password.value,
    };

    // console.log(JSON.stringify(user_data));
    const response = await fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_data),
    });
    const data = await response.json();
    console.log(data);

    if (data.message === 'User created') {
        status_message.hidden = false;
        status_message.textContent = 'Successfully Registered! Redirecting. . .'
        setTimeout(() => { switch_pages(); }, 3000);
        setTimeout(() => { status_message.hidden = true; }, 10000);
    } else {
        status_message.hidden = false;
        status_message.textContent = 'This account already exists.\nConsider logging in instead.'
        setTimeout(() => { status_message.hidden = true; }, 10000);
    }
}

// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();

    // save user data
    save_user_data();

    // clear inputs
    signup_form.reset();
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