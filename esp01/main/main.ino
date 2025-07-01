#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "********"
#define STAPSK "********"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);

const char* available_requests[] = {
  "/front-door/0",
  "/front-door/1",
  "/bath-door/0",
  "/bath-door/1",
  "/fan/0",
  "/fan/1",
  "/bedroom-light/0",
  "/bedroom-light/1",
  "/bath-light/0",
  "/bath-light/1",
  "/tv/0",
  "/tv/1",
  "/env",
  "/mode/movie",
  "/mode/disco",
  "/mode/wakeup",
  "/mode/empty",
  "/mode/automatic",
  "/mode/manual",
};

const int available_request_num = sizeof(available_requests) / sizeof(available_requests[0]);

void setup() {
  Serial.begin(115200);

  // prepare LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 0);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.println();
  Serial.println(F("WiFi connected"));

  // Start the server
  server.begin();
  Serial.println(F("Server started"));

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.accept();
  if (!client) { return; }

  client.setTimeout(5000);  // default is 1000

  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);

  // Match the request
  bool valid_req = false;
  for (int i = 0; i < available_request_num; i++) {
    if (req.indexOf(available_requests[i]) != -1) {
      Serial.println(available_requests[i]);
      valid_req = true;
    }
  }

  if (!valid_req) {
    Serial.println(F("Invalid request"));
  }

  // read/ignore the rest of the request
  // do not client.flush(): it is for output only, see below
  while (client.available()) {
    // byte by byte is not very efficient
    client.read();
  }

  // Send the response to the client
  // it is OK for multiple small client.print/write,
  // because nagle algorithm will group them into one single packet
  client.print(F("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\nCommand options:<br>"));
  for (int i = 0; i < available_request_num; i++) {
    client.print(F("<br>Send <a href='http://"));
    client.print(WiFi.localIP());
    client.print(available_requests[i]);
    client.print(F("'>"));
    client.print(available_requests[i]);
    client.print(F("</a>"));
  }
  // The client will actually be *flushed* then disconnected
  // when the function returns and 'client' object is destroyed (out-of-scope)
  // flush = ensure written data are received by the other side
}
