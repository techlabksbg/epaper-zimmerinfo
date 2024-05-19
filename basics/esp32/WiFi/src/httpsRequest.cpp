#include <WiFiClientSecure.h>
#include "ISRG_Root_X1.h"
#include <HTTPClient.h>

// From https://randomnerdtutorials.com/esp32-https-requests/

// server is epaper.tech-lab.ch
// url is for instance /anzeige?mac=asdf?volt=3.83
// buffer is memory to write response body to
// bufLen is the maximal length of accepted response.
int httpsRequest(String url, char * buffer, int bufLen) {
    if (!url.startsWith("https://")) {
        Serial.println("URL must start with https://");
        return -1;
    }
    int servEnd = url.indexOf("/",8);
    String server = url.substring(8,servEnd);
    String location = url.substring(servEnd);
    WiFiClientSecure client;
    client.setCACert(isrg_root_x1);
    Serial.print("\nStarting connection to server ");
    Serial.println(server);
    if (!client.connect(server.c_str(), 443)) {
        Serial.println("Connection failed!");
        return -1;
    }
    Serial.println("Connected to server!");
    Serial.print("Accessing location ");
    Serial.println(location);
    // Make a HTTP request:
    client.print("GET ");
    client.print(url);
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

    unsigned int start = millis(); 
    int timeout = 5000;
    int bytesRead = 0;
    for (char * ptr = buffer; ptr<buffer+bufLen && ptr<buffer+contentLength; ptr++) {
        int tm = timeout;
        while (client.available()==0 && tm>0) {
            delay(1);
            tm--;
        }
        if (tm<=0 || millis()-start>20000) {
            return ptr-buffer;
        }
        *ptr = client.read();
        bytesRead++;
    }
    Serial.printf("Read %d Bytes into buffer\n", bytesRead);
    client.stop();
    return bytesRead;
}

// https://randomnerdtutorials.com/esp32-http-get-post-arduino/

int httpRequest(String url, char * buffer, int bufLen) {
    if (!url.startsWith("http://")) {
        Serial.println("URL must start with http://");
        return -1;
    }
    HTTPClient http;

    Serial.printf("Accesssing %s\n", url.c_str());
    http.begin(url.c_str());
    int httpResponseCode = http.GET();
    Serial.printf("Response Code %d\n",httpResponseCode);
    int bytesRead = 0;
    if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        bytesRead = payload.length();
        strncpy(buffer, payload.c_str(), bufLen);
    } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
        return 0;
    }
    // Free resources
    http.end();
    return bytesRead;
}

int request(String url, char * buffer, int bufLen) {
    if (url.startsWith("https://")) {
        return httpsRequest(url, buffer, bufLen);
    } else {
        return httpRequest(url, buffer, bufLen);
    }
}