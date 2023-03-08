// grabbing elements for manipulation
// const log_in_page = document.querySelector('.log_in');
const crawling_form = document.querySelector('.crawling_input_container form');
const crawling_inputs = document.querySelectorAll('.crawling_input_container form input');
// const search_engine_selection = document.querySelector('#search_engine_selection')
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
    const response = await fetch('http://127.0.0.1:5500/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_data),
    });
    const data = await response.JSON();
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

// go to sign up page if user is new
// const switch_pages = () => {
//     log_in_page.hidden = false;
//     sign_up_page.hidden = true;
// }

// EventListener
crawling_form.addEventListener('submit', process_form_data);
// login_here.addEventListener('click', switch_pages)