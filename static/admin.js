// grabbing elements for manipulation
const register_user = document.querySelector('.info2 button');
const crawler_page = document.querySelector('.crawler_page');
const log_out = document.querySelector('.log_out');
const admin_chamber = document.querySelector('.admin_panel_container');
const log_in_page = document.querySelector('.log_in');
const sign_up_page = document.querySelector('.sign_up');
const crawling_input_container = document.querySelector('.crawling_input_container');
const users_list = document.querySelector('.admin_panel_container .users_list');

// fetching users' data
export const fetch_users_data = async () => {
    
    const response = await fetch('http://127.0.0.1:5000/users');
    const data = await response.json();
    console.log(data);

    // populating DOM with users' data
    users_list.textContent = '';
    
    data.forEach(user => {
        // create elements
        const username = document.createElement('div');
        username.classList.add('username');
        username.textContent = `Username: ${user.username}`;
        const email = document.createElement('div');
        email.classList.add('email');
        email.textContent = `Email: ${user.email}`;
        const password = document.createElement('div');
        password.classList.add('password');
        password.textContent = `Password: ${user.password}`;
        const delete_btn = document.createElement('button');
        delete_btn.classList.add('delete');
        delete_btn.textContent = `delete user`;
        const user_body = document.createElement('li');
        user_body.classList.add('user');
        // putting them together
        user_body.append(username, email, password, delete_btn);
        users_list.appendChild(user_body);

        // erase user's account when delete button is clicked
        delete_btn.addEventListener('click', async () => {
            const user_email = { email: user.email };
            const response = await fetch('http://127.0.0.1:5000/delete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(user_email),
            });
            const reply = await response.json();
            console.log(reply);

            fetch_users_data();
        });
    });

}

fetch_users_data();


// take admin to the sign up page
const to_sign_up_or_login_page = (page) => {
    admin_chamber.hidden = true;
    page.parentElement.hidden = false;
    page.parentElement.children[0].hidden = true;
    page.parentElement.children[1].hidden = true;
    page.hidden = false;
}

// take admin to the crawler's page
const to_crawler_page = () => {
    admin_chamber.hidden = true;
    crawling_input_container.hidden = false;
}

// EventListeners
register_user.addEventListener('click', () => { to_sign_up_or_login_page(sign_up_page) })
crawler_page.addEventListener('click', to_crawler_page)
log_out.addEventListener('click', () => { to_sign_up_or_login_page(log_in_page) })