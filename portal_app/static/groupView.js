window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    let categories_names = document.querySelectorAll(".singleGroup");
    // categories_divs = document.querySelectorAll(".categoryPath");
    categories_names.forEach(el=>{
        console.log(el);
        console.dir(el);
        console.log('nd');
        el.addEventListener('mouseenter', evt => {
            let list = el.lastElementChild
            list.classList.toggle('hide')
        })
        el.addEventListener('mouseleave', evt => {
            let list = el.lastElementChild
            list.classList.toggle('hide')
        })
    })
});