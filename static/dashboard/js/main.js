const table = document.getElementById("myTable");
const rows = table.getElementsByTagName("tr");

for (let i = 0; i < rows.length; i++) {
  if (i % 2 == 0) {
    rows[i].style.backgroundColor = "#DEEEFA";
  } else {
    rows[i].style.backgroundColor = "whitesmoke";
  }
}
