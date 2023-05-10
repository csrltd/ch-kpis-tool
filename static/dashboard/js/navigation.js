const menuIcon = document.querySelector(".mobile-menu-icon")
const closeMenuIcon = document.querySelector(".close-mobile-menu-icon")
const leftMenu = document.querySelector(".left-menu")

closeMenuIcon.style.display="none"
menuIcon.addEventListener('click', () => {
    leftMenu.style.display="block"
    closeMenuIcon.style.display="block"
    menuIcon.style.display="none"
})

closeMenuIcon.addEventListener('click', () => {
    leftMenu.style.display="none"
    closeMenuIcon.style.display="none"
    menuIcon.style.display="block"
})


const rchDropDown = document.querySelector('#rhcDropDown')
const laborDropDown = document.querySelector('#laborDropDown')
const hspDropDown = document.querySelector('#hspDropDown')
const rhcDropDownContent = document.querySelector('.rhcdropdown-content')
const hspDropDownContent = document.querySelector('.hspdropdown-content')
const laborDropDownContent = document.querySelector('.labordropdown-content')

rchDropDown.addEventListener('click', () => {
    rhcDropDownContent.classList.toggle("hidden")
    rhcDropDownContent.classList.add("dropdown-content-class")

})

hspDropDown.addEventListener('click', () => {
    hspDropDownContent.classList.toggle("hidden")
    hspDropDownContent.classList.add("dropdown-content-class")
})

laborDropDown.addEventListener('click', () => {
    laborDropDownContent.classList.toggle("hidden")
    laborDropDownContent.classList.add("dropdown-content-class")
})


//profile popup
profile = document.querySelector(".profile")
profilePopup = document.querySelector(".profile-popup")
closePopup = document.querySelector(".close-text")

profile.addEventListener('click', () => {
    profilePopup.style.visibility = "visible"
})

profilePopup.addEventListener("mouseover", () => {
    profilePopup.style.visibility = "visible"
})

profilePopup.addEventListener("mouseout", () => {
    profilePopup.style.visibility = "hidden"
})

closePopup.addEventListener('click', () => {
    profilePopup.style.visibility = "hidden"
})