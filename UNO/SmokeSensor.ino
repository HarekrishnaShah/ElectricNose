//Gas Sensors
int Gas[15];
int sendTime = 0;

void setup(){
  Serial.begin(9600);
  //pinMode(controlPin,OUTPUT);
  //digitalWrite(controlPin, HIGH);//High Vol Close
}

void loop(){
  int readNum = 0;
  if (Serial.available()){
    readNum = Serial.read();
    if(readNum != '\r'){
      sendTime = sendTime * 10 + (readNum - 48);
    }
    else{
      for(int j = 0; j < sendTime; j ++){
        for(int i = 0; i < 15; i ++){
          Gas[i] = analogRead(i);
        }
        //float smoke_float = wet_int / 204.6;
        Serial.print("GAS_A0=");Serial.print(Gas[0]);Serial.print(" ");
        Serial.print("GAS_A1=");Serial.print(Gas[1]);Serial.print(" ");
        Serial.print("GAS_A2=");Serial.print(Gas[2]);Serial.print(" ");
        Serial.print("GAS_A3=");Serial.print(Gas[3]);Serial.print(" ");
        Serial.print("GAS_A4=");Serial.print(Gas[4]);Serial.print(" ");
        Serial.print("GAS_A5=");Serial.print(Gas[5]);Serial.print(" ");
        Serial.print("GAS_A6=");Serial.print(Gas[6]);Serial.print(" ");
        Serial.print("GAS_A7=");Serial.print(Gas[7]);Serial.print(" ");
        Serial.print("GAS_A8=");Serial.print(Gas[8]);Serial.print(" ");
        Serial.print("GAS_A9=");Serial.print(Gas[9]);Serial.print(" ");
        Serial.print("GAS_A10=");Serial.print(Gas[10]);Serial.print(" ");
        Serial.print("GAS_A11=");Serial.print(Gas[11]);Serial.print(" ");
        Serial.print("GAS_A12=");Serial.print(Gas[12]);Serial.print(" ");
        Serial.print("GAS_A13=");Serial.print(Gas[13]);Serial.print(" ");
        Serial.print("GAS_A14=");Serial.print(Gas[14]);Serial.print(" \r\n");
        delay(100);
      }
      sendTime = 0;    
    }
    
  }
}
