window.addEventListener('DOMContentLoaded', (event) => {
    let counters = document.querySelectorAll(".unseenMessages");
    counters.forEach(counter=>{
        let name = counter.previousElementSibling
        name.style.fontWeight='bold'
    })
})

