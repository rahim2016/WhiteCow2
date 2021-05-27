const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".table-area");
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");

tableOutput.style.display = "none";

const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";

  

    fetch("/search-deals", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          
          data.forEach((item) => {
              
            tbody.innerHTML += `
                <tr>
                <td>${item.name}</td>
                <td>${item.date}</td>
               <td> <a type="button" class="btn btn-outline-success btn-md"  href="">View Deal</a></td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
    noResults.style.display = "none";
  }
});





