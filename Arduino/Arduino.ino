// Inertial Naigation Module

double p[3]; // relative position
double v[3]; // speed

double t1;

double dt;

double x, y, z, a, b, c;


void setup() {
}



void loop() {
  
  // refresh x, y, z, a, b, c from sensor
  
  double accel[3]; // acceleration related to horizon
  double dv[3]; // change in velocity vec related to horizon
  double L = sqrt(x * x + y * y + z * z);
  
  accel[0] = L * cos(sqrt(x * x + y * y) / L + a) * cos(sqrt(x * x + z * z) / L + c);
  accel[1] = L * cos(sqrt(x * x + y * y) / L + a) * cos(sqrt(y * y + z * z) / L + b);
  accel[2] = L * cos(sqrt(y * y + z * z) / L + b) * cos(sqrt(x * x + z * z) / L + c);
  
  dt = micros() - t1;
  
  dv[0] = accel[0] * dt;
  dv[1] = accel[1] * dt;
  dv[2] = accel[2] * dt;
  
  p[0] += (v[0] + 0.5 * dv[0]) * dt;
  p[1] += (v[1] + 0.5 * dv[1]) * dt;
  p[2] += (v[2] + 0.5 * dv[2]) * dt;

  v[0] += dv[0];
  v[1] += dv[1];
  v[2] += dv[2];
  t1 = micros();
}
