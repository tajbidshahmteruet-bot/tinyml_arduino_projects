#include <Arduino_LED_Matrix.h>
#include <math.h>

ArduinoLEDMatrix matrix;

const int ROWS = 8;
const int COLS = 13;

uint8_t frame[ROWS][COLS];

void clearFrame() {
  for (int r = 0; r < ROWS; r++) {
    for (int c = 0; c < COLS; c++) {
      frame[r][c] = 0;
    }
  }
}

void drawSineWave(float phase) {
  clearFrame();

  for (int col = 0; col < COLS; col++) {

    // Normalize column to range 0 → 2π
    float x = ((float)col / (COLS - 1)) * 2.0 * PI + phase; // 6/(13-1)*2*PI = 0.5*2*PI = PI

    float y = sin(x);  // range: -1 to +1 

    // Map y to row (invert for display)
    int row = (int)((1.0 - y) * (ROWS - 1) / 2.0);

    // Safety clamp
    if (row < 0) row = 0;
    if (row >= ROWS) row = ROWS - 1;

    frame[row][col] = 7;
  }

  matrix.draw(&frame[0][0]);
}

void setup() {
  matrix.begin();
  matrix.setGrayscaleBits(3);
}

void loop() {
  static float phase = 0.0;

  drawSineWave(phase);

  phase += 0.3;   // speed
  if (phase > 2 * PI) {
    phase -= 2 * PI;
  }

  delay(120);
}