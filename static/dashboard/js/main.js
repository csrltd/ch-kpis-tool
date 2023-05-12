const table = document.getElementById("myTable");
const rows = table.getElementsByTagName("tr");
const tableHeader = document.querySelector(".tableHead");

for (let i = 0; i < rows.length; i++) {
  if (i % 2 == 0) {
    rows[i].style.backgroundColor = "#DEEEFA";
  } else {
    rows[i].style.backgroundColor = "whitesmoke";
  }
}
tableHeader.style.backgroundColor = "#00AEEF";
