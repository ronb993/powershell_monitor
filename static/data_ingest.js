function draw() {
    window.onload =function(){
      draw_connections();
      var canvas = document.getElementById('map');
      var ctx = canvas.getContext("2d");
      var img = document.getElementById("map_image");
      ctx.drawImage(img, 0, 0, img.width, img.height);
    };
};

function draw_players(items, enemy, friend, scav, player){
  var line_color = "rgb(230, 16, 238)";
  var map_info = [2254, 1916, 3.731];
  var zeroX = map_info[0];
  var zeroY = map_info[1];
  var scale = map_info[2];
  const length = 400;
  const s_length = 200;
  const yaw_offset = 0;
  var pi = Math.PI;
  player = player || 0;
  enemy = enemy || 0;
  friend = friend || 0;
  scav = scav || 0;
  items = items || 0;
  const pcanvas = document.getElementById('player');
  if (pcanvas.getContext){
    const pctx = pcanvas.getContext("2d");
    pctx.font = "25px Helvetica"
    pctx.fillStyle = "rgb(255,255,51)";
    // clear canvas for refreshing new positions
    pctx.clearRect(0, 0, pcanvas.width, pcanvas.height);
    if (items){
      for (pos of items){
        x = zeroX + (pos[0] * scale);
        y = zeroY - (pos[1] * scale);
        pctx.fillText(pos[2], x+10, y);
        pctx.beginPath();
        pctx.arc(x, y, 300/60, 0, Math.PI * 2);
        pctx.fill();
        pctx.closePath();
      }
    }
    pctx.fillStyle = "rgb(255, 0, 0)";
    pctx.strokeStyle = line_color;
    pctx.lineWidth = 2;
    if (enemy){
      for (pos of enemy){
        x = zeroX + (pos[0] * scale);
        y = zeroY - (pos[1] * scale);
        z = Math.ceil(pos[2]);
        yaw_radians = (pos[3] * (pi/180));
        let x_offset = length * Math.cos(yaw_radians + yaw_offset);
        let y_offset = length * Math.sin(yaw_radians + yaw_offset);
        pctx.fillText(`${pos[4]} H:${z}`, x-40, y-15);
        pctx.beginPath();
        pctx.moveTo(x, y);
        pctx.lineTo(x + x_offset, y + y_offset);
        pctx.stroke();
        pctx.closePath();
        pctx.moveTo(x, y);
        pctx.arc(x, y, 300/40, 0, Math.PI * 2);
        pctx.fill();
        pctx.closePath();
      }
    }
    pctx.fillStyle = "rgb(0, 255, 0)";
    pctx.strokeStyle = line_color;
    pctx.lineWidth = 2;
    if (friend){
      for (pos of friend){
        x = zeroX + (pos[0] * scale);
        y = zeroY - (pos[1] * scale);
        z = Math.ceil(pos[2]);
        yaw_radians = (pos[3] * (pi/180));
        let x_offset = length * Math.cos(yaw_radians + yaw_offset);
        let y_offset = length * Math.sin(yaw_radians + yaw_offset);
        pctx.fillText(`${pos[4]} H:${z}`, x-40, y-15);
        pctx.beginPath();
        pctx.moveTo(x, y);
        pctx.lineTo(x + x_offset, y + y_offset);
        pctx.stroke();
        pctx.closePath();
        pctx.moveTo(x, y);
        pctx.arc(x, y, 300/40, 0, Math.PI * 2);
        pctx.fill();
        pctx.closePath();
      }
    }
    pctx.fillStyle = "rgb(255, 255, 255)";
    pctx.strokeStyle = "rgb(255, 255, 255)";
    pctx.lineWidth = 2;
    if (scav){
      for (pos of scav){
        x = zeroX + (pos[0] * scale);
        y = zeroY - (pos[1] * scale);
        z = Math.ceil(pos[2]);
        yaw_radians = (pos[3] * (pi/180));
        let x_offset = s_length * Math.cos(yaw_radians + yaw_offset);
        let y_offset = s_length * Math.sin(yaw_radians + yaw_offset);
        pctx.fillText(`H:${z}`, x-15, y-20);
        pctx.beginPath();
        pctx.moveTo(x, y);
        pctx.lineTo(x + x_offset, y + y_offset);
        pctx.stroke();
        pctx.closePath();
        pctx.moveTo(x, y);
        pctx.arc(x, y, 300/40, 0, Math.PI * 2);
        pctx.fill();
        pctx.closePath();
      }
    }
    pctx.fillStyle = "rgb(0, 255, 255)";
    pctx.strokeStyle = line_color;
    pctx.lineWidth = 2;
    if (player){
      for (pos of player){
        x = zeroX + (pos[0] * scale);
        y = zeroY - (pos[1] * scale);
        z = Math.ceil(pos[2]);
        yaw_radians = (pos[3] * (pi/180));
        let x_offset = length * Math.cos(yaw_radians + yaw_offset);
        let y_offset = length * Math.sin(yaw_radians + yaw_offset);
        pctx.fillText(`Luke H:${z}`,x-35, y-15);
        pctx.beginPath();
        pctx.moveTo(x, y);
        pctx.lineTo(x + x_offset, y + y_offset);
        pctx.stroke();
        pctx.closePath();
        pctx.moveTo(x, y);
        pctx.arc(x, y, 300/40, 0, Math.PI * 2);
        pctx.fill();
        pctx.closePath();
      }
    }
  }
};


var socket = io.connect();
socket.on("updateSensorData", function (data) {
       draw_players(data.items, data.enemy, data.friend, data.scav, data.player);

});




