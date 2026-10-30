# ESPHome Setup

Quick start for the configurations in this repository. They are tested with ESPHome 2026.10.1.

## What you need

- An IoTextra module on a supported carrier (see the [compatibility matrix](../README.md)).
- [ESPHome](https://esphome.io/guides/installing_esphome/) installed on your computer.
- A USB cable. IoTsmart ESP32-S3 has a native USB port (no UART bridge).

## Steps

1. Download the YAML file for your module and carrier from [Configs](../Configs).
2. Create `secrets.yaml` next to it:

   ```yaml
   wifi_ssid: "your network name"
   wifi_password: "your network password"
   ```

3. Build and flash: `esphome run <file>.yaml`. Flash the first firmware over USB; later updates can go over the air.
4. Open the device in Home Assistant, or use its web page on port 80.

## Notes

- Do not use `board: esp32-s3-devkitc-1` for IoTsmart ESP32-S3. Use `variant: esp32s3`, `flash_size: 4MB` and
  `psram: mode: quad`, as in the configurations here.
- Windows: if your user name contains a space, ESP-IDF builds can fail. Set `ESPHOME_ESP_IDF_PREFIX` and
  `ESPHOME_DATA_DIR` to a path without spaces.
- Channels are active-low on the HOST line, so pins are declared with `inverted: true`.
