#include <OneWire.h>                                  //for temp
#include <DallasTemperature.h>                        //for temp
#include <SoftwareSerial.h>                           //for EC



// temp
#define ONE_WIRE_BUS 3  // temperature pin

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

float Celcius=0;
float Fahrenheit=0;
String bufferStr="";
String ecCommand = "";

// EC
#define rx 8                                          //EC fake rx (digital)
#define tx 9                                          //EC fake tx must be pwm
#define ECswitch 7                                    //EC mosfet switch

SoftwareSerial myserial(rx, tx);                      //define how the soft serial port is going to work

String inputstring = "";                              //a string to hold incoming data from the PC
String sensorstring = "";                             //a string to hold the data from the Atlas Scientific product
boolean input_string_complete = false;                //have we received all the data from the PC
boolean sensor_string_complete = false;               //have we received all the data from the Atlas Scientific product

void writeString(String stringData) { // Used to serially push out a String with Serial.write()

  for (int i = 0; i < stringData.length(); i++)
  {
    Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }

}// end writeString


// Air temp + humidty
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTTYPE           DHT22     // DHT 22 (AM2302)
#define DHTPIN            10         // Pin which is connected to the DHT sensor.

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;
// end Air temp + humidity

void setup(void)
{
  
  Serial.begin(9600);
  sensors.begin();                                    // temp

  myserial.begin(9600);                               // EC. set baud rate for the software serial port to 9600
  inputstring.reserve(10);                            //set aside some bytes for receiving data from the PC
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
  pinMode(ECswitch, OUTPUT);                          //EC mosphet switch pin
  digitalWrite(ECswitch, HIGH);                       //set to on
  

  // air temp + humidity
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000;
}

void loop(void)
{ 
  //check serial in
  //Serial.write("Hello Pi, from Arduino\n");
  if (Serial.available() > 0)
  {
    bufferStr=Serial.readString();
    Serial.println(bufferStr);
  }
  
  //TEMP
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Fahrenheit=sensors.toFahrenheit(Celcius);
  bufferStr="C "+String(Celcius)+" F  "+String(Fahrenheit)+"\n";
  writeString(bufferStr);
  delay(1000);

  // EC
  //send command to get reading.  use most recent temperature reading.
  ecCommand = "RT,"+String(Celcius);
  myserial.print(ecCommand);
  myserial.print('\r');
  delay(1000);


  // get output from EC device
  for (int i = 0; i < 1000; i++){                     // outer to loop to keep checking for data from EC
    if (myserial.available() > 0) {                     //if we see that the Atlas Scientific product has sent a character
      char inchar = (char)myserial.read();              //get the char we just received
      sensorstring += inchar;                           //add the char to the var called sensorstring
      if (inchar == '\r') {                             //if the incoming character is a <CR>
        sensor_string_complete = true;                  //set the flag
      }
    }
  
    if (sensor_string_complete == true) {               //if a string from the Atlas Scientific product has been received in its entirety
      if (isdigit(sensorstring[0]) == false) {          //if the first character in the string is a digit
        Serial.println(sensorstring);                   //send that string to the PC's serial monitor
      }
      else                                              //if the first character in the string is NOT a digit
      {
        print_EC_data();                                //then call this function 
      }
      sensorstring = "";                                //clear the string
      sensor_string_complete = false;                   //reset the flag used to tell if we have received a completed string from the Atlas Scientific product
    }
  }

  // Temp and Humidity
  // Delay between measurements.
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;  
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println("Error reading temperature!");
  }
  else {
    Serial.print("Temperature: ");
    Serial.print(event.temperature);
    Serial.println(" *C");
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("Error reading humidity!");
  }
  else {
    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");
  }


}// end main


void print_EC_data(void) {                            //this function will parse the string  

  char sensorstring_array[30];                        //we make a char array
  char *EC;                                           //char pointer used in string parsing
  char *TDS;                                          //char pointer used in string parsing
  char *SAL;                                          //char pointer used in string parsing
  char *GRAV;                                         //char pointer used in string parsing
  float f_ec;                                         //used to hold a floating point number that is the EC
  
  sensorstring.toCharArray(sensorstring_array, 30);   //convert the string to a char array 
  EC = strtok(sensorstring_array, ",");               //let's pars the array at each comma
  TDS = strtok(NULL, ",");                              //let's pars the array at each comma
  SAL = strtok(NULL, ",");                              //let's pars the array at each comma
  GRAV = strtok(NULL, ",");                           //let's pars the array at each comma

  Serial.print("EC:");                                //we now print each value we parsed separately
  Serial.println(EC);                                 //this is the EC value

  Serial.print("TDS:");                               //we now print each value we parsed separately
  Serial.println(TDS);                                //this is the TDS value

  Serial.print("SAL:");                               //we now print each value we parsed separately
  Serial.println(SAL);                                //this is the salinity value

  Serial.print("GRAV:");                              //we now print each value we parsed separately
  Serial.println(GRAV);                               //this is the specific gravity
  Serial.println();                                   //this just makes the output easier to read
  
//f_ec= atof(EC);                                     //uncomment this line to convert the char to a float
}
