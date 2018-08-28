#include <ArduinoJson.h>

#include <SparkFun_TB6612.h>
#include <Wire.h>
#include <Adafruit_TCS34725.h>

#include <Adafruit_APDS9960.h>

#define BUFF_SIZE 256
#define SERIAL_BAUDRATE 115200
#define PUB_PERIOD 50 // in ms
#define TERM_CHARACTER '\n'

#define SPEED 100


#define AIN1 3
#define BIN1 D6
#define AIN2 1
#define BIN2 D5
#define PWMA D8
#define PWMB D7
#define STBY D0

const int offsetA = -1;
const int offsetB = 1;
Motor m_left = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
Motor m_right = Motor(BIN1, BIN2, PWMB, offsetB, STBY);

Adafruit_APDS9960 apds;
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_24MS, TCS34725_GAIN_1X);

uint16_t lr, lg, lb, lc;
uint16_t rr, rg, rb, rc;

StaticJsonBuffer<BUFF_SIZE> outJsonBuffer;
unsigned long last_pub = 0;
unsigned long last_cmd = 0;

StaticJsonBuffer<BUFF_SIZE> inJsonBuffer;
char inBuff[BUFF_SIZE];
int I = 0;


void setup() {
  Serial.begin(SERIAL_BAUDRATE);

  if(!apds.begin()){
    Serial.println("failed to initialize device! Please check your wiring.");
  }
  else Serial.println("Device initialized!");

  //enable color sensign mode
  apds.enableColor(true);

  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }
}

void loop() {
  // Publish State
  unsigned long t = millis();
  if ((t - last_pub) >= PUB_PERIOD) {
    JsonObject &state = buildJsonState();

    state["last_command"] = last_cmd;

    state.printTo(Serial);
    Serial.println();
    last_pub = t;
  }

  // Read Command
  int n = Serial.available();
  while (n--) {
     char c = Serial.read();
     if (c == TERM_CHARACTER || I >= BUFF_SIZE -1) {

        inJsonBuffer.clear();
        JsonObject &cmd = inJsonBuffer.parseObject(inBuff);

        if (cmd.success()) {
          handleCommands(cmd);
        }

        clearInBuffer();

     } else {
        inBuff[I++] = c;
     }
  }
}

void handleCommands(JsonObject &cmd) {
  last_cmd = millis();

  JsonObject &wheels = cmd["wheels"];

  if (wheels.success()) {
    if (wheels.containsKey("left")) {
      int left_speed = wheels["left"];

      if (left_speed == 0) {
        m_left.brake();
      } else {
        left_speed = min(max(left_speed, 0), 200);
        m_left.drive(left_speed);
      }
    }

    if (wheels.containsKey("right")) {
      int right_speed = wheels["right"];

      if (right_speed == 0) {
        m_right.brake();
      } else {
        right_speed = min(max(right_speed, 0), 200);
        m_right.drive(right_speed);
      }
    }
  }
}


JsonObject& buildJsonState() {
  outJsonBuffer.clear();

  JsonObject &root = outJsonBuffer.createObject();
  JsonObject &ls = root.createNestedObject("light_sensor");

  while(!apds.colorDataReady()) {
    delay(1);
  }
  apds.getColorData(&lr, &lg, &lb, &lc);
  tcs.getRawData(&rr, &rg, &rb, &rc);

  JsonArray &left = ls.createNestedArray("left");
  left.add(lr);
  left.add(lg);
  left.add(lb);
  left.add(lc);

  JsonArray &right = ls.createNestedArray("right");
  right.add(rr);
  right.add(rg);
  right.add(rb);
  right.add(rc / 40);

  root["timestamp"] = millis();

  return root;
}

void clearInBuffer() {
  for (int i=0; i<BUFF_SIZE; i++) {
    inBuff[i] = '\0';
  }
  I = 0;
}
