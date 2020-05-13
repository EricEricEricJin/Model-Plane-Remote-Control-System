/**
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
 *      analyze the address
 *      uodate ARP table
 *      IF sender frame is empty THEN
 *        shallow-copy the frame to sender
 *      ENDIF // 如果阻塞的话就把包丢掉 不需要告诉发送者
 *      init the receiver port
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

/**
 * Frame format:
 * [start: 1][source: 4][target: 4][frame_no: 8][len: 6][data: 40][checksum: 1]
 * 
 * 校验不需要switch管 switch需要看的只是source和target
 * switch不可以更改数据帧
 */

# define PACK_SIZE 8 // byte
# define T_INTERVAL 24 // micro sec
# define PORT_NUM 7

struct frame {
  byte* data;
  bool isSendRecv;
  unsigned long prev_time;
  byte curr_index;
};


frame* send_queue;
frame* recv_queue;

frame* recv_port;
frame* send_port;

byte* arp_table;
// [port, addr, ..., ..., port, addr]


byte anal_addr(byte* data, byte curr_port_no) {
  byte source = (*(data) & (0b01111000)) >> 3 ;
  byte target = (*(data) & (0b00000111)) << 1 + (*(data + 1) & (0b10000000)) >> 7;
  byte tar_port_no = 255;
  for (byte i = 0; i < PORT_NUM; i++) {
    if (*(arp_table + 2 * i + 1) == source) {
      *(arp_table + 2 * i) = curr_port_no; // always update arp table
    }
    if (*(arp_table + 2 * i + 1) == target) {
      tar_port_no = *(arp_table + 2 * i);
    }
  }
  return tar_port_no;
}

bool checksum(byte* data) {
  bool sum = 0;
  for (byte i = 0; i < PACK_SIZE * 8 - 1; i++) {
    if (( *( data + int(i / 8) ) & ( byte(1) << (7 - (i % 8) ) ) ) > 0) {
      sum += 1;
    }
  }
  if (sum == (bool) (*(data + PACK_SIZE - 1) & (0b00000001) ) ) {
    return true;
  } else {
    return false;
  }
}


void setup() {
  send_queue = (frame*)malloc(sizeof(frame) * PORT_NUM);
  recv_queue = (frame*)malloc(sizeof(frame) * PORT_NUM);

  arp_table = (byte*)malloc(sizeof(byte) * PORT_NUM * 2);

  for (byte i = 0; i < PORT_NUM; i++) {
    pinMode(i * 2, INPUT_PULLUP);
    pinMode(i * 2 + 1, OUTPUT);
  }
}

void loop() {
  for (byte port = 0; port < PORT_NUM; port++) {
    recv_port = recv_queue + port;
    send_port = send_queue + port;
    
    if (recv_port -> isSendRecv == 0) {
      // Not R/S, Listen to beginning
      if (digitalRead(port * 2) == HIGH) { // get high level
        recv_port -> isSendRecv = 1;
        recv_port -> data = (byte*)malloc(sizeof(byte) * PACK_SIZE);
        *(recv_port -> data + 0) &= (1 << 8);
        recv_port -> curr_index = 1;
        recv_port -> prev_time = micros();
      }
    } else if ((micros() - recv_port -> prev_time) >= T_INTERVAL) {
      // in time, recv now
      // bool recv_raw; // read from IO
      if (digitalRead(port * 2) == HIGH) {
        // high level
        *(recv_port -> data + int( (recv_port -> curr_index) / 8 ) ) &= (1 << (7 - (recv_port -> curr_index) % 8));
      } else {
        // low level do nothing
      }
      recv_port -> curr_index += 1;
      recv_port -> prev_time = micros();

      if (recv_port -> curr_index >= PACK_SIZE * 8) {
        // recv full
        if (checksum(recv_port -> data)) {
          byte tar_port_no = anal_addr(recv_port -> data, port);
          if (tar_port_no != 255) {
            frame* tar_port = (send_queue + tar_port_no);
            if (tar_port -> isSendRecv == 0) {
              // copy to send
              // analyze addr
              
              tar_port -> isSendRecv = 1;
              tar_port -> data = recv_port -> data;
              tar_port -> curr_index = 0; 
            } else {
              free(recv_port -> data);
            }
          } else {
            free(recv_port -> data);
          }          
        } else {
          free(recv_port -> data);
        }
        
        recv_port -> isSendRecv = 0;
        recv_port -> curr_index = 0;
      }
    }
    
    if (send_port -> isSendRecv && (micros() - send_port -> prev_time) >= T_INTERVAL) {
      bool send_raw;
      if ((*(send_port -> data + ( int(send_port -> curr_index / PACK_SIZE) ) ) & (1 << (7 - (send_port -> curr_index) % 8))) > 0) {
        digitalWrite(port * 2 + 1, HIGH);
      } else {
        digitalWrite(port * 2 + 1, LOW);
      }
      // send send_raw here
      
      
      send_port -> curr_index += 1;
      send_port -> prev_time = micros();

      if (send_port -> curr_index >= PACK_SIZE * 8) {
        digitalWrite(port * 2 + 1, LOW);
        free(send_port -> data);
        send_port -> curr_index = 0;
        send_port -> isSendRecv = 0;
      }
    }
    
  }
}
