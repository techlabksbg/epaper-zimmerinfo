#pragma once

// server is epaper.tech-lab.ch
// url is for instance /anszeige?mac=asdf?volt=3.83
// buffer is memory to write response body to
// bufLen is the maximal length of accepted response.
int httpsRequest(String server, String location, char * buffer, int bufLen);