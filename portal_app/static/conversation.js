window.addEventListener('DOMContentLoaded', (event) => {

    let elem = document.querySelector(".conversation");
    elem.scrollTop = elem.scrollHeight;

    let myMsgs = document.querySelectorAll(".myMessageContent");
    let not_myMsgs = document.querySelectorAll(".toMeMessageContent");


    myMsgs.forEach(msg => {
        msg.addEventListener('mouseenter', e => {
            msg.lastElementChild.classList.remove('hide')
        })
        msg.addEventListener('mouseleave', e => {
            msg.lastElementChild.classList.add('hide')
        })
    })


    not_myMsgs.forEach(msg => {
        msg.addEventListener('mouseenter', e => {
            msg.lastElementChild.classList.remove('hide')
        })
        msg.addEventListener('mouseleave', e => {
            msg.lastElementChild.classList.add('hide')
        })
    })
})

