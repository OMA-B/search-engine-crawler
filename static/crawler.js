// grabbing elements for manipulation
const log_in_page = document.querySelector('.log_in');
const crawling_form = document.querySelector('.crawling_input_container form');
const crawling_inputs = document.querySelectorAll('.crawling_input_container form input');
const bottom_options = document.querySelector('.crawler_bottom_options');
const crawling_input_container = document.querySelector('.crawling_input_container');
const admin_chamber = document.querySelector('.admin_panel_container');
const csv_link = document.querySelector('.crawling_input_container .csv_link');
const status_message = document.querySelector('.crawling_input_container .status_message');

// scanning inputs for validity
export const check_validity = (inputs) => {
    inputs.forEach(input => {
        if (input.value !== '' && !input.checkValidity()) {
            input.style.border = '1px solid red';
        } else if (input.value !== '' && input.checkValidity()) {
            input.style.border = '1px solid rgb(92, 137, 233)';
        } else {
            input.style.border = '1px solid rgb(92, 137, 233)';
        }
    })
}
setInterval(() => { check_validity(crawling_inputs) }, 1000);

// fetch csv file
export const fetch_csv_file = async () => {
    const file_response = await fetch('http://127.0.0.1:5000/csv');
    const file_data = await file_response.blob();
    const url = window.URL.createObjectURL(file_data);
    csv_link.setAttribute('href', url);
}

// collecting user's data
const save_user_data = async () => {
    const user_data = {
        search_option: crawling_form.search_engine_selection.value,
        keyword: crawling_form.keyword.value,
        page_depth: crawling_form.page_depth.value,
        max_search_number: crawling_form.max_search_number.value,
    };

    // post data to start crawling
    csv_link.parentElement.hidden = true;
    status_message.hidden = false;

    try {
        const response = await fetch('http://127.0.0.1:5000/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user_data),
        });
        const data = await response.json();

        fetch_csv_file();

        status_message.hidden = true;
        csv_link.parentElement.hidden = false;
    } catch (error) {
        if (error) {
            status_message.textContent = 'Engine inaccessible. Retry later, or try different search.';
            setTimeout(() => {
                status_message.hidden = true;
                fetch_csv_file();
                csv_link.parentElement.hidden = false;
                status_message.textContent = 'Crawling In Progress. . .';
            }, 10000);
        }
    }

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
bottom_options.children[1].addEventListener('click', () => { to_login_page(log_in_page) });