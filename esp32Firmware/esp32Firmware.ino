#include "sbus.h"

// SBUS receiver on Serial1, RX = GPIO 16, TX = GPIO 17
bfs::SbusRx sbus_rx(&Serial1, 16, 17, true, false);
bfs::SbusData data;

constexpr uint32_t USB_BAUD_RATE = 115200;
constexpr int NUM_CHANNELS = 16;

void setup() {
    Serial.begin(USB_BAUD_RATE);
    sbus_rx.Begin();
}

void loop() {
    if (sbus_rx.Read()) {
        data = sbus_rx.data();

        // Send all 16 channels as one CSV line.
        for (int i = 0; i < NUM_CHANNELS; i++) {
            if (i > 0) {
                Serial.print(',');
            }

            Serial.print(data.ch[i]);
        }

        Serial.println();
    }
}
