int x_acc_count= 0;
int y_acc_count= 0;
int z_acc_count= 0;

String last_dir_x = "";
String last_dir_y = "";
String last_dir_z = "";


void detectJump(float xAcc, float yAcc, float zAcc) {

 /***********************************************   
  *    X JUMP
  **********************************************/
  if(xAcc > 1.25 && !(xAcc >0 && xAcc < 0.0001)) {
        //Serial.println(xAcc);
        x_acc_count = x_acc_count +1;
        last_dir_x = "pos";
  }
  else {
    if(last_dir_x == "pos" && x_acc_count > 30) {
        //Serial.println(acc_pos);
        if(millis() - lastActionMillis > ACTION_TIME_BUFFER) {
          Serial.println(FORWARD_JUMP);
          lastActionMillis = millis();
          lastAction = FORWARD_JUMP;
        }
    }
    x_acc_count = 0;
    last_dir_x = "neg";
  }

 /***********************************************   
  *    Y JUMP
  **********************************************/

  if(yAcc > .75 && !(yAcc >0 && yAcc < 0.0001)) {
        y_acc_count = y_acc_count +1;
        last_dir_y = "pos";
  }
    else {
      if(last_dir_y == "pos" && y_acc_count > 20) {
          //Serial.println(acc_pos);
          if(millis() - lastActionMillis > ACTION_TIME_BUFFER) {
            Serial.println(SIDE_JUMP);
            lastActionMillis = millis();
            lastAction = SIDE_JUMP;
          }
      }
      y_acc_count = 0;
      last_dir_y = "neg";
    }

 /***********************************************   
  *    Z JUMP
  **********************************************/
 if(zAcc > 2 && !(zAcc >0 && zAcc < 0.0001)) {
    //Serial.println(xAcc);
    z_acc_count = z_acc_count +1;
    last_dir_z = "pos";
  }
  else {
    if(last_dir_z == "pos" && z_acc_count > 20) {
        //Serial.println(acc_pos);
        // if jump twice and program hasn't started yet.
        if(millis() - lastActionMillis > ACTION_TIME_BUFFER) {
          if(lastAction == UP_JUMP) {
            Serial.println("start");
//             start_sonic_pi = true; 
          }
          Serial.println(UP_JUMP);
          lastActionMillis = millis();
          lastAction = UP_JUMP;
        }
    }
    z_acc_count = 0;
    last_dir_z = "neg";
  }
}


  
