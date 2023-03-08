// grabbing elements for manipulation
const users_del_btn = document.querySelectorAll('.users_list .user .delete');
const register_user = document.querySelector('.info2 button');
const crawler_page = document.querySelector('.crawler_page');
const log_out = document.querySelector('.log_out');
const admin_chamber = document.querySelector('.admin_panel_container');
const log_in_page = document.querySelector('.log_in');
const sign_up_page = document.querySelector('.sign_up');
const crawling_input_container = document.querySelector('.crawling_input_container');

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

// delete respective user on click
users_del_btn.forEach(del_btn => {
    del_btn.addEventListener('click', () => {
        console.log(del_btn.parentElement.parentElement);
    })
});