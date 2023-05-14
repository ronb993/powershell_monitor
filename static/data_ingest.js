  function receive_data(data){
  let json_data = data;
  console.log(json_data);
  let col = [];
  for (let i = 0; i < json_data.length; i++) {
    for (let key in json_data[i]) {
      if (col.indexOf(key) === -1) {
        col.push(key);
      }
    }
  }

    // Create table.
  const table = document.createElement("table");

    // Create table header row using the extracted headers above.
  let tr = table.insertRow(-1);                   // table row.

  for (let i = 0; i < col.length; i++) {
    let th = document.createElement("th");      // table header.
    th.innerHTML = col[i];
    tr.appendChild(th);
  }

    // add json data to the table as rows.
  for (let i = 0; i < json_data.length; i++) {

    tr = table.insertRow(-1);

    for (let j = 0; j < col.length; j++) {
      let tabCell = tr.insertCell(-1);
      tabCell.innerHTML = json_data[i][col[j]];
      }
  }

    // Now, add the newly created table with json data, to a container.
  const divShowData = document.getElementById('showData');
  divShowData.innerHTML = "";
  divShowData.appendChild(table);
};

var socket = io.connect();
socket.on("updateData", function (data) {
       receive_data(data.pshell);

});









