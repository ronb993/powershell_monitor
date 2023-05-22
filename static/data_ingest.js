function receive_data(data){
let json_data = data;
/*console.log(json_data);*/
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

// create ElementID for highlighted connections
let high_light = document.getElementById('highLight');
// add json data to the table as rows.
for (let i = 0; i < json_data.length; i++) {
  let tr = table.insertRow(-1);
  for (let j = 0; j < col.length; j++) {
    let tabCell = tr.insertCell(-1);
    if(json_data[i]['NewProcess'] == true){
      tabCell.innerHTML = `<span class='highLight'>${json_data[i][col[j]]}</span>`;
    }
    else{
      tabCell.innerHTML = json_data[i][col[j]];
    }
    console.log(json_data[i]['NewProcess']);
  }
}
// Now, add the newly created table with json data, to a container.
const divShowData = document.getElementById('showData');
divShowData.innerHTML = "";
divShowData.appendChild(table);
};

/* function push_proc(data){
let json_data = data;
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
const divShowProc = document.getElementById('showProc');
divShowProc.innerHTML = "";
divShowProc.appendChild(table);
};
*/
function get_users(data){
  let user_list = data;
  let ip_list = document.getElementById('showUsers');
  ip_list.innerHTML = "Users Connected:";
  user_list.forEach((item)=>{
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(item));
    ip_list.appendChild(li);
  });
};

var socket = io.connect();
$(document).ready(socket.on("updateData", function (data) {
       receive_data(data.conn);
       //push_proc(data.proc);
       get_users(data.users);

}));









