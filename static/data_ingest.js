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

// add json data to the table as rows.
for (let i = 0; i < json_data.length; i++) {
  let tr = table.insertRow(-1);
  for (let j = 0; j < col.length; j++) {
    let tabCell = tr.insertCell(-1);
    if(json_data[i]['NewConnection'] == true){
      tabCell.innerHTML = `<span class='highLight'>${json_data[i][col[j]]}</span>`;
    }
    else{
      tabCell.innerHTML = json_data[i][col[j]];
    }
  }
}
// Now, add the newly created table with json data, to a container.
const divShowData = document.getElementById('showData');
divShowData.innerHTML = "";
divShowData.appendChild(table);
};

function get_badip(data){
  let ip_list = data;
  let bad = document.getElementById('showBad');
  let nobad = document.getElementById('noBad');
  bad.innerHTML = "";
  nobad.innerHTML = "No Bad IPs Connected via TCP";
  if(ip_list.length > 0){
    nobad.innerHTML = "";
    ip_list.forEach((item)=>{
      console.log(item);
      let li = document.createElement("li");
      li.appendChild(document.createTextNode('Local IP: '+item[0]));
      li.appendChild(document.createTextNode(' Local Port:'+item[1]));
      li.appendChild(document.createTextNode(' Remote IP:'+item[2]));
      li.appendChild(document.createTextNode(' Remote Port:'+item[3]));
      li.appendChild(document.createTextNode(' Time:'+item[4]));
      li.appendChild(document.createTextNode(' Process:'+item[5]));
      bad.appendChild(li);
    })
  }
};

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
       get_users(data.users);
       get_badip(data.badip);

}));









