/**
 * @file arduino_usb_to_led.ino
 * @brief High-speed, non-blocking serial receiver for 3-channel audio visualization.
 */

// PWM-supported pins for frequency bands
const uint8_t ledBass1 = 9;   // 50-100 Hz (Deep Bass)
const uint8_t ledBass2 = 10;  // 100-300 Hz (Upper Bass / Mid)
const uint8_t ledTiz   = 11;  // 5000-7000 Hz (High-Pass / Treble)

uint8_t buffer[3];
uint8_t dataIndex = 0;
bool isSyncing = true; // Wait for the 255 sync byte

void setup() {
    Serial.begin(115200);
    pinMode(ledBass1, OUTPUT);
    pinMode(ledBass2, OUTPUT);
    pinMode(ledTiz, OUTPUT);
}

void loop() {
    // Non-blocking state machine for instant serial processing
    while (Serial.available() > 0) {
        uint8_t incomingByte = Serial.read();
        
        // 255 is our strict synchronization frame byte
        if (incomingByte == 255) { 
            dataIndex = 0; 
            isSyncing = false; 
        }
        else if (!isSyncing) {
            buffer[dataIndex] = incomingByte;
            dataIndex++;
            
            // Once all 3 brightness values arrive, write to LEDs
            if (dataIndex == 3) {
                analogWrite(ledBass1, buffer[0]);
                analogWrite(ledBass2, buffer[1]);
                analogWrite(ledTiz,   buffer[2]);
                
                isSyncing = true; // Wait for the next sync byte
            }
        }
    }
}