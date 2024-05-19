#pragma once

// url is like https://epaper.tech-lab.ch/anzeige?mac=asdf?volt=3.83
// buffer is memory to write response body to
// bufLen is the maximal length of accepted response.
int httpsRequest(String url, char * buffer, int bufLen);
int httpRequest(String url, char * buffer, int bufLen);
int request(String url, char * buffer, int bufLen);