/*
 * SETUP    
 *  allocate [[frame being processed by receiver], [], [], ..., []]
 *  allocate [[frame being processed by sender], [], [], ..., []]
 * ENDSETUP
 * 
 * LOOP
 *  FOR ports
 *    IF isRecving AND is_in_time THEN
 *      read from the port and write into frame being processed
 *    ENDIF
 *    IF recv_process_frame full THEN
 *      IF sender frame is empty THEN
 *        shallow-copy the frame to sender
 *      ENDIF // 如果阻塞的话就把包丢掉
 *      init(free) the receiver port
 *    ENDIF
 *    
 *    IF sender frame is not empty
 *      send a bit (and modify index)
 *    ENDIF
 *    IF sender frame index is > xx THEN
 *      index <- 0
 *      isSending <- 0
 *    ENDFOR
 *  ENDFOR
 * ENDLOOP
*/



# define PACK_SIZE 8 // byte
# define T_INTERVAL 24 // micro sec


struct recv_port {
  byte port_no;
  byte* frame;
  byte index;
  unsigned long prev_time;
  bool isRecving;
};

struct send_port {
  byte* frame;
  byte index;
  unsigned long prev_time;
  byte port_no;
};

byte*** frame_queue;

recv_port* port_recv_list;

void setup() {
  frame_queue = 
  
  port_recv_list = (recv_port*)malloc(sizeof(recv_port) * 7);
  for (byte i = 0; i < 7; i++) {
    (port_recv_list + i) -> frame = (byte*)malloc(sizeof(byte) * PACK_SIZE);
    (port_recv_list + i) -> index = 0;
    (port_recv_list + i) -> isRecving = false;
    (port_recv_list + i) -> port_no = i;
  }
}

void loop() {
  for (byte i = 0; i < 7; i++) {
    if (true) { // 读出电平
      (port_recv_list + i) -> isRecving = 1;
    }
    if ((port_recv_list + i) -> isRecving && (micros() - (port_recv_list + i) -> prev_time) >= T_INTERVAL) {
      // 读出电平
      if (true) {
        *((port_recv_list + i) -> frame + int((port_recv_list + i) -> index / 8)) &= (1 << (port_recv_list + i) -> index % 8);
      }
      (port_recv_list + i) -> prev_time = micros();
      (port_recv_list + i) -> index += 1;
    }
    if ((port_recv_list + i) -> index >= PACK_SIZE * 8) {
      // fasong wanbi
      (port_recv_list + i) -> isRecving = 0;
      
    }
    
    
  }
}
