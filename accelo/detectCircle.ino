/*
 *  For future work we don't need bin_averages array 
 *  since we only use the last two bins at any given point
 */

const String INCREASING = "increasing";
const String DECREASING = "decreasing"; 

const int NUM_READINGS_PER_BIN = 20;
float curr_bin[NUM_READINGS_PER_BIN];
int curr_bin_len = 0;
int bin_averages_curr_len = 0;
const int BIN_AVERAGES_MAX_LEN = 2;
float bin_averages[BIN_AVERAGES_MAX_LEN];
int MIN_CIRCLE_BINS = 250; //min number of steps need to complete a circle 
float STEP_CAP = 25;
float STEP_MIN = .01;

String roll_direction = INCREASING; 
String rel_to_last = INCREASING; 
float diff_from_last = 0; 
int conseq_steps = 0; 

/* *********************************************************
 *  
 *                    HELPER FUNCTIONS 
 *                    
 ***********************************************************/

bool isAtEdge(float n1, float n2) {
  if((n1 >= 360 - STEP_CAP && n2) || (n1 <= 0 + STEP_CAP && n2 >= 360 - STEP_CAP)) {
    return true; 
  }
  else  {
    return false; 
  }
}

bool isNeg(float n) {
  return n < 0; 
}
bool isPos(float n) {
  return n >= 0; 
}


void detectCircle(float roll) {
//  Serial.println(roll);
  if(bin_averages_curr_len == BIN_AVERAGES_MAX_LEN) {
    bin_averages_curr_len = 0;
  }
  if(curr_bin_len == NUM_READINGS_PER_BIN) {
//    Serial.print("100th reading: ");
    float curr_bin_average = average(curr_bin, curr_bin_len); 
//    Serial.println(curr_bin_average);
//    Serial.println(bin_averages_curr_len); 
    bin_averages[bin_averages_curr_len] = curr_bin_average; 
    bin_averages_curr_len = bin_averages_curr_len + 1; 
    curr_bin_len = 0;
    checkForCircle();
  }
  else {
    curr_bin[curr_bin_len] = roll;
    curr_bin_len = curr_bin_len + 1; 
  }
}

void checkForCircle() {
  if(bin_averages_curr_len > 1) {
    float prev_val = bin_averages[bin_averages_curr_len - 2]; 
    float curr_val = bin_averages[bin_averages_curr_len - 1]; 
    bool isAtEdge_ = isAtEdge(prev_val, curr_val); 
    if(!isAtEdge_) {
      diff_from_last = prev_val - curr_val; 
    }
    else if(isAtEdge_ && prev_val <= 0 + STEP_CAP) {
      rel_to_last = DECREASING; 
    }
    else {
      rel_to_last = INCREASING; 
    }
    if(isNeg(diff_from_last)) {
      rel_to_last = INCREASING; 
    }
    else {
      rel_to_last = DECREASING; 
    }
//    Serial.print("diff_to_last: "); 
//    Serial.println(diff_from_last); 
    if(abs(diff_from_last) <= STEP_CAP && abs(diff_from_last) >= STEP_MIN)  {
//      Serial.print("conseq bins: "); 
      //Serial.println(conseq_steps); 
      conseq_steps = conseq_steps + 1; 
    }
    else {
      if(!(abs(diff_from_last) <= STEP_CAP)){
//        Serial.println("\n\n too BIG \n\n");
//        Serial.print("prev: ");
//        Serial.print(prev_val);
//        Serial.print("curr ");
//        Serial.print(curr_val);
//        
      }
      if(!(abs(diff_from_last) >= STEP_MIN)){
//        Serial.println("\n\n too SMALL \n\n");
      }
      if(conseq_steps >= MIN_CIRCLE_BINS) {
          Serial.print("circle:");
          Serial.println(conseq_steps);
          lastAction = CIRCLE; 
//        Serial.println("\n\n******************************");
//        Serial.println("DETECT CIRCLE");
//        Serial.println("******************************\n\n"); 
      }
      conseq_steps = 0; 
    }
  }
}


float average (float * array, int len)  // assuming array is int.
{
  float sum = 0L ;  // sum will be larger than an item, long for safety.
  for (int i = 0 ; i < len ; i++)
    sum += array [i] ;
  return  sum / len ;  // average will be fractional, so float may be appropriate.
}
