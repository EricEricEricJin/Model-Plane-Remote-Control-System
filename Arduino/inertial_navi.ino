// Inertial Naigation Module

# include <Wire.h>
# define SLAVE_ADDR 0x72
double p[3]; // relative position
double v[3]; // speed

double t1;

double dt;

double x, y, z, a, b, c;

void send_data() {
  byte p_send[6];
  p_send[0] = (byte)((int)p[0] / 256);
  p_send[1] = (byte)((int)p[0] - p_send[0] * 256);
  p_send[2] = (byte)((int)p[1] / 256);
  p_send[3] = (byte)((int)p[1] - p_send[2] * 256);
  p_send[4] = (byte)((int)p[2] / 256);
  p_send[5] = (byte)((int)p[2] - p_send[4] * 256);
  Wire.write(p_send, 6);
}

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(send_data);
}


void loop() {
  
  /*
    refresh x, y, z, a, b, c from MPU 6050 sensor here.
  */
  
  double accel[3];
  double dv[3];
  double L = sqrt(x * x + y * y + z * z);
  
  accel[0] = L * cos(sqrt(x * x + y * y) / L + a) * cos(sqrt(x * x + z * z) / L + c);
  accel[1] = L * cos(sqrt(x * x + y * y) / L + a) * cos(sqrt(y * y + z * z) / L + b);
  accel[2] = L * cos(sqrt(y * y + z * z) / L + b) * cos(sqrt(x * x + z * z) / L + c);
  
  dt = micros() - t1;
  if (dt < 0) {
    dt = 4294967295 - t1 + micros(); // int type overflow after about 71 min.
  }
  t1 = micros();
  
  dv[0] = accel[0] * dt;
  dv[1] = accel[1] * dt;
  dv[2] = accel[2] * dt;
  
  p[0] += (v[0] + 0.5 * dv[0]) * dt;
  p[1] += (v[1] + 0.5 * dv[1]) * dt;
  p[2] += (v[2] + 0.5 * dv[2]) * dt;

  v[0] += dv[0];
  v[1] += dv[1];
  v[2] += dv[2];
}
