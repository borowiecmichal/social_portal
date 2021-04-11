window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

    let hidePostBtn = document.querySelector("#hidePostsBtn");
    let hidePhotosBtn = document.querySelector("#hidePhotosBtn");

    hidePostBtn.addEventListener('click', evt => {
        let toHide = document.querySelectorAll(".singlePost, .likes");
        console.log(toHide);
        toHide.forEach(item => {
            item.classList.toggle('hide');
        })
        if (hidePostBtn.innerText === 'Ukryj posty')
            hidePostBtn.innerText = 'Pokaż posty'
        else if (hidePostBtn.innerText === 'Pokaż posty')
            hidePostBtn.innerText = 'Ukryj posty'
    })

    hidePhotosBtn.addEventListener('click', evt => {
        let toHide = document.querySelectorAll(".singlePhoto");

        toHide.forEach(item => {
            item.classList.toggle('hide');
        })

        if (hidePhotosBtn.innerText === 'Ukryj zdjęcia')
            hidePhotosBtn.innerText = 'Pokaż zdjęcia'
        else if (hidePhotosBtn.innerText === 'Pokaż zdjęcia')
            hidePhotosBtn.innerText = 'Ukryj zdjęcia'
    })

    let photos = document.querySelectorAll("img"); //hide and show button
    photos.forEach(item=>{
        console.log(item);
        item.addEventListener('mousedown', e=>{
            item.parentElement.classList.add('fullscreen-mode');
            let escBtn = document.createElement("button");
            console.log(escBtn);
            escBtn.innerText='X';
            item.parentElement.appendChild(escBtn);
            escBtn.addEventListener('click', event=>{
                item.parentElement.classList.remove('fullscreen-mode');
                escBtn.remove()
            })
        })
    })
});