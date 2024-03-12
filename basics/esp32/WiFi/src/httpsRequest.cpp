#include <WiFiClientSecure.h>
#include "ISRG_Root_X1.h"


// From https://randomnerdtutorials.com/esp32-https-requests/

// server is epaper.tech-lab.ch
// url is for instance /anszeige?mac=asdf?volt=3.83
// buffer is memory to write response body to
// bufLen is the maximal length of accepted response.
int httpsRequest(String server, String location, char * buffer, int bufLen) {
    WiFiClientSecure client;
    client.setCACert(test_root_ca);
    Serial.println("\nStarting connection to server...");
    if (!client.connect(server.c_str(), 443)) {
        Serial.println("Connection failed!");
        return -1;
    }
    Serial.println("Connected to server!");
    // Make a HTTP request:
    client.print("GET ");
    client.print(location);
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(server);
    client.println("Connection: close");
    client.println();

    int contentLength = -1;
    while (client.connected()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
        if (line.startsWith("Content-Length: ")) {
            contentLength = line.substring(16).toInt();
            Serial.printf("I have length: %d\n", contentLength);
        }
        if (line == "\r") {
            Serial.println("headers received");
            break;
        }
    }
    // if there are incoming bytes available
    // from the server, read them and print them:
    
    int timeout = 5000;
    int bytesRead = 0;
    for (char * ptr = buffer; ptr<buffer+bufLen && ptr<buffer+contentLength; ptr++) {
        int tm = timeout;
        while (client.available()==0 && tm>0) {
            delay(1);
            tm--;
        }
        if (tm<=0) {
            return ptr-buffer;
        }
        *ptr = client.read();
        bytesRead++;
    }
    Serial.printf("Read %d Bytes into buffer\n", bytesRead);
    client.stop();
    return bytesRead;
}
