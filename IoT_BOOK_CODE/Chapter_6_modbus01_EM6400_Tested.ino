// ****** DEFINES ******
#define MAX485_DE      3
#define MAX485_RE_NEG  2


// ****** INCLUDES ******
#include <ModbusMaster.h>
//#include <SPI.h>

// ****** GLOBALS ******
ModbusMaster node;  // instantiate ModbusMaster object
float reg1;     // will store the float value found at 3910/3911
float reg2;     // will store the float value found at 3914/3915
int low_word;   // this will hold the low 16-bit resgter value after a read
int high_word;  // this will hold the high 16-bit resgter value after a read

// converting to floating point - union structure
union u_tag {
  int bdata[2];
  float flotvalue;
} uniflot;

// ****** Transmission Functions ******
void preTransmission()
{
  digitalWrite(MAX485_RE_NEG, 1);
  digitalWrite(MAX485_DE, 1);
  Serial.println("preTransmission");
}

void postTransmission()
{
  digitalWrite(MAX485_RE_NEG, 0);
  digitalWrite(MAX485_DE, 0);
  Serial.println("postTransmission");
}


// ****** STANDARD ARDUINO SETUP FUNCTION ******
void setup() {
  
  // make pins 2 and 3 output pins for Max485 flow control
  pinMode(MAX485_RE_NEG, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);

  // Init in receive mode
  digitalWrite(MAX485_RE_NEG, 0);
  digitalWrite(MAX485_DE, 0);

  Serial.begin(9600);     // TX0/RX0 serial monitor
  Serial1.begin(9600);   // TX1/RX1 Modbus comms

  // Modbus slave ID = 1
  node.begin(1, Serial1);

  // Callbacks allow us to configure the RS485 transceiver correctly
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  Serial.println("Hello World");

}

// ****** STANDARD ARDUINO LOOP FUNCTION ******
void loop() {

  uint8_t result;


  // Read Line to Neutral Voltage
  result = node.readHoldingRegisters(3910, 2);
  //result = node.readHoldingRegisters(1, 2);
   if (result == node.ku8MBSuccess) 
  {

    high_word = node.getResponseBuffer(0x00);
    low_word = node.getResponseBuffer(0x01);
    
    uniflot.bdata[1] = low_word;    // Modbus data 16-bit low word
    uniflot.bdata[0] = high_word;   // Modbus data 16-bit high word

    reg1 = uniflot.flotvalue;
    
    Serial.print("Line to Neutral Voltage: ");
    Serial.println(reg1);
    
  } 
//  node.clearResponseBuffer();
  delay(500);   // small delay between reads
  
  //Read Frequency
  result = node.readHoldingRegisters(3914, 2);
  if (result == node.ku8MBSuccess)
  {
    high_word = node.getResponseBuffer(0x00);
    low_word = node.getResponseBuffer(0x01);
    
    uniflot.bdata[1] = low_word;    // Modbus data 16-bit low word
    uniflot.bdata[0] = high_word;   // Modbus data 16-bit high word

    reg2 = uniflot.flotvalue;
    
    Serial.print("Frequency: ");
    Serial.println(reg2);
  }

  delay(2000);    // repeat reading every 2 seconds
  node.clearResponseBuffer();
  
}
