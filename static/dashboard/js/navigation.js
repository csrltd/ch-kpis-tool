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
