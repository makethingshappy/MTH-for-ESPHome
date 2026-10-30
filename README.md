# MTH for ESPHome

ESPHome configurations for [Make Things Happy](https://makethingshappy.io) IoTextra modules on IoTsmart and IoTbase platforms.

## ESPHome Compatibility Matrix

<!-- IOTEXTRA_ESPHOME_COMPATIBILITY_START -->
# IoTextra ESPHome Compatibility
| IoTextra Module | IoTsmart ESP32-S3 | IoTsmart XIAO + XIAO ESP32-S3 | IoTbase PICO + Waveshare ESP32-S3-Pico | IoTbase NANO + Waveshare ESP32-S3-NANO | IoTbase Feather + Adafruit ESP32-C6 Feather |
|---|:---:|:---:|:---:|:---:|:---:|
| Input | [![Config](https://img.shields.io/badge/Config-green)](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-input-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Relay | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Relay2 | [🔶](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-relay2-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| SSR Small | [![Config](https://img.shields.io/badge/Config-green)](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-ssr-small-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| MOSFET2 | [![Config](https://img.shields.io/badge/Config-green)](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-mosfet2-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Quadro | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Octal | [![Config](https://img.shields.io/badge/Config-green)](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-octal-v3-04-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Octal2 | [![Config](https://img.shields.io/badge/Config-green)](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-octal2-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Octal3 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Octal4 | [🔶](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-octal4-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Analog | [🔶](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-analog-v3-12-iotsmart-esp32s3-v2-01-i2c.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Analog2 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Analog3 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |
| Combo | [🔶](https://github.com/makethingshappy/MTH-for-ESPHome/blob/main/Configs/IoTsmart_ESP32-S3/iotextra-combo-v3-04-iotsmart-esp32s3-v2-01-gpio.yaml) | 🔲 | 🔲 | 🔲 | 🔲 |
| Combo2 | 🔲 | 🔲 | 🔲 | 🔲 | 🔲 |

**Legend:**
- [![Config](https://img.shields.io/badge/Config-green)]() — config available and verified on hardware, click to open
- 🔶 — config published, not yet verified on hardware
- 🔲 — Planned

<!-- IOTEXTRA_ESPHOME_COMPATIBILITY_END -->

## How the configurations are built

Every configuration is derived from two `host-map.yaml` files that live next to the hardware design files:
the carrier's (which GPIO drives each HOST line `AP0`–`AP7`, and the I2C bus) and the module's (which HOST line or
I2C expander channel drives each channel).
For IoTsmart ESP32-S3 2.01 the carrier file is
[ESP32-S3/v.2.01/host-map.yaml](https://github.com/makethingshappy/IoTsmart/blob/main/ESP32-S3/v.2.01/host-map.yaml);
module files are in the [IoTextra-Digital](https://github.com/makethingshappy/IoTextra-Digital),
[IoTextra-Analog](https://github.com/makethingshappy/IoTextra-Analog) and
[IoTextra-Combo](https://github.com/makethingshappy/IoTextra-Combo) repositories.

[`Tools/esphome_check.py`](Tools/esphome_check.py) checks a configuration against both files.

## File naming

`iotextra-<module>-v<module version>-<carrier>-v<carrier version>-<gpio|i2c>.yaml`

For example `iotextra-mosfet2-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml` is IoTextra MOSFET2 3.02 on IoTsmart ESP32-S3 2.01,
controlled through the HOST GPIO lines. Module and carrier versions are part of the name, so configurations for
different hardware revisions can coexist.
Do not rename published files: the `dashboard_import` URL inside a firmware points to the file name.

## Notes

- Octal: the configuration assumes solder bridge SB2 closed (AP4 drives RL1).
- Setup instructions: [Documentation/Setup.md](Documentation/Setup.md).

## License

[MIT](LICENSE)
