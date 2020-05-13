/**
 * Send and receive data through the switch
 */

/*
  Send
    parameter: byte* data
    return: void

  Receive
    parameter: bool block
    return: byte*
*/
/*
 * Frame format:
 * [start: 1][source: 4][target: 4][frame_no: 8][len: 6][data: 40][checksum: 1]
 */


#ifdef _N_W__
#define _N_W__

#include <Arduino.h>

struct frame {
  byte* data;
  bool isSendRecv;
  unsigned long prev_time;
  byte curr_index;
};

class Network {
  private:
    frame* frames;
  public:
    void send_to(byte* data, byte tar_addr);
    byte* recv(byte);
}

#endif
