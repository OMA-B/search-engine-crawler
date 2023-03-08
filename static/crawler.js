// grabbing elements for manipulation
const log_in_page = document.querySelector('.log_in');
const crawling_form = document.querySelector('.crawling_input_container form');
const crawling_inputs = document.querySelectorAll('.crawling_input_container form input');
const bottom_options = document.querySelector('.crawler_bottom_options');
const crawling_input_container = document.querySelector('.crawling_input_container');
const admin_chamber = document.querySelector('.admin_panel_container');
// const status_message = document.querySelector('.sign_up .status_message');
// const login_here = document.querySelector('.login_option button');
// const sign_up_page = document.querySelector('.sign_up');

// scanning inputs for validity
const check_validity = () => {
    crawling_inputs.forEach(input => {
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
        search_option: crawling_form.search_engine_selection.value,
        keyword: crawling_form.keyword.value,
        page_depth: crawling_form.page_depth.value,
        max_search_number: crawling_form.max_search_number.value,
    };

    // console.log(JSON.stringify(user_data));
    const response = await fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_data),
    });
    const data = await response.json();
    console.log(data);
}

// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();

    // save user data
    save_user_data();

    // clear inputs
    crawling_form.reset();
}

// log user out and back to the login page
const to_login_page = (page) => {
    crawling_input_container.hidden = true;
    page.parentElement.hidden = false;
    page.parentElement.children[0].hidden = true;
    page.parentElement.children[1].hidden = true;
    page.hidden = false;
}

// take admin back to admin chamber
const to_admin_chamber = () => {
    crawling_input_container.hidden = true;
    admin_chamber.hidden = false;
}

// EventListener
crawling_form.addEventListener('submit', process_form_data);
bottom_options.children[0].addEventListener('click', to_admin_chamber);
bottom_options.children[1].addEventListener('click', () => { to_login_page(log_in_page) })
// login_here.addEventListener('click', switch_pages)