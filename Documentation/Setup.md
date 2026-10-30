# ESPHome Setup Guide

This guide takes an IoTextra module on an IoTsmart carrier from the box to a running ESPHome device.
The configurations in this repository are tested with ESPHome 2026.10.1 (Python 3.13).

## Table of Contents

1. [What You Need](#1-what-you-need)
2. [Powering the Module](#2-powering-the-module)
3. [Install ESPHome](#3-install-esphome)
4. [Choose Your Config](#4-choose-your-config)
5. [Prepare `secrets.yaml`](#5-prepare-secretsyaml)
6. [First Flash over USB](#6-first-flash-over-usb)
7. [Adopt in Home Assistant or the ESPHome Dashboard](#7-adopt-in-home-assistant-or-the-esphome-dashboard)
8. [Updates over the Air](#8-updates-over-the-air)
9. [Module Notes](#9-module-notes)
10. [Verify Everything Is Working](#10-verify-everything-is-working)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. What You Need

**Hardware**

- An IoTextra module on a supported carrier. The modules and carriers with ready configs are listed in the [ESPHome Compatibility Matrix](../README.md#esphome-compatibility-matrix) in the repository README.
- A 5 V DC power supply for the PWR connector (see [Powering the Module](#2-powering-the-module)).
- A USB cable for the first flash. IoTsmart ESP32-S3 uses the native USB port of the Waveshare ESP32-S3-Tiny,
  connected through the Tiny Adapter Board (USB Type-C). The adapter and cable are not included with the carrier.

**Software**

- [ESPHome](https://esphome.io/guides/installing_esphome/), as a command-line tool or as the ESPHome Device Builder add-on for Home Assistant.
- A 2.4 GHz Wi-Fi network.

## 2. Powering the Module

IoTsmart ESP32-S3 runs from a **+5 V DC** supply.

- Connect the supply to the two-pin **PWR** connector (JST S2B-PH-K-S, 2.00 mm pitch). Check the polarity markings on the board.
  The carrier has reverse-polarity protection, but do not rely on it.
- The total current, including everything powered from the module's HOST connector (the mezzanine), should not exceed **1 A**.
  The carrier itself draws about 25 mA.
- USB and PWR can be connected at the same time. On the Waveshare ESP32-S3-Tiny the USB VBUS reaches the 5 V rail
  through a Schottky diode, so the supply on PWR does not feed back into the USB port.
- Powering from USB alone is fine for flashing and bench tests. The voltage on the 5 V rail is then about 0.3–0.4 V lower
  than the USB voltage, and the current is limited by the USB port. Use the PWR connector for real loads.

## 3. Install ESPHome

Command line (a virtual environment is recommended):

```bash
python3 -m venv esphome-env
source esphome-env/bin/activate        # Windows: esphome-env\Scripts\activate
pip install esphome
esphome version
```

Alternatively, install the ESPHome Device Builder add-on in Home Assistant and use it in place of the `esphome` commands below.

## 4. Choose Your Config

1. Open the [ESPHome Compatibility Matrix](../README.md#esphome-compatibility-matrix) in the repository README and find your module in the row and your carrier in the column.
2. Click the **Config** button. It leads to the YAML file in [`Configs/`](../Configs).
3. Download that file. Do not rename it (see below).

File names follow the pattern

```
iotextra-<module>-v<module version>-<carrier>-v<carrier version>-<gpio|i2c>.yaml
```

The version numbers are the board revisions printed on your module and carrier. `gpio` configs drive the module through the
HOST lines directly, `i2c` configs use an I2C chip on the module.

> **Do not rename the files.** Each config contains a `dashboard_import` URL that points to its own file name in this
> repository. Firmware built from the config remembers that URL, and the ESPHome Dashboard uses it to offer updates.

The pin and I2C assignments in each file come from the `host-map.yaml` of the carrier and of the module
(linked from the [IoTextra Software Compatibility](https://github.com/makethingshappy/.github/blob/main/IOTEXTRA_SOFTWARE_COMPATIBILITY.md) table).

## 5. Prepare `secrets.yaml`

Create `secrets.yaml` next to the config file:

```yaml
wifi_ssid: "your network name"
wifi_password: "your network password"
```

## 6. First Flash over USB

1. Connect the Tiny Adapter to your computer and to the FPC connector on IoTsmart.
2. From the folder with the config and `secrets.yaml`, run:

   ```bash
   esphome run iotextra-mosfet2-v3-02-iotsmart-esp32s3-v2-01-gpio.yaml
   ```

   Use the file name of your own config. The first build downloads the toolchain and takes several minutes.
3. When asked, choose the serial port of the device. ESPHome compiles, uploads and then shows the device log.
4. The log shows the Wi-Fi connection and the IP address. The device is now on your network.

**If the port is not found or the upload fails**, put the chip into bootloader mode with the buttons on the Tiny Adapter:
hold **BOOT**, press and release **RUN** (reset), then release BOOT. Run the command again.

## 7. Adopt in Home Assistant or the ESPHome Dashboard

**Home Assistant.** The device is discovered automatically. Open *Settings → Devices & services*, find the discovered
ESPHome device and click **Add**. Every channel of the module appears as an entity.

**ESPHome Dashboard.** A flashed device that has not been adopted appears under *Discovered*. **Adopt** copies the
configuration into your dashboard, so you can edit it and update the device from there.

If the device cannot join your Wi-Fi network, it starts its own access point named `<name> Fallback Hotspot`. Connect to it from
a phone or computer and the captive portal lets you enter the correct network.

The configs also include a small **web page on port 80** (`http://<ip-address>/`) that shows all channels and lets you
switch outputs without Home Assistant.

## 8. Updates over the Air

After the first flash, run the same command again:

```bash
esphome run <your-config>.yaml
```

and choose the network device instead of the serial port. The firmware is uploaded over Wi-Fi.
If the device is not reachable over the network, flash it over USB again as in [step 6](#6-first-flash-over-usb).

To update the config itself (for example after a new version is published in this repository), download the new file and
replace your copy. Keep your own changes in your own copy of the file.

## 9. Module Notes

- **Active-low channels.** The channels of the IoTextra modules are active-low on the HOST line (output on = pin low).
  The configs declare the pins with `inverted: true`, so *on* in ESPHome means *on* at the module. The configs set the outputs to **off** at start-up (`restore_mode: ALWAYS_OFF`).
- **IoTextra Octal.** The config assumes solder jumper **SB2** is closed, which is the factory default: HOST line AP4 then drives relay RL1.
  If you have closed **SB1** instead, AP4 becomes the I/O expander interrupt and RL1 will not work.
- **IoTextra Analog.** Each channel has a range setting in the `substitutions` block at the top of the file
  (gain, scale factor and unit). The comment above the block lists the values for each input range
  (0–10 V, 0–5 V, 0–0.5 V, 4–20 mA and so on). Set them to match the jumpers of your module.
- **I2C bus.** The HOST I2C bus of IoTsmart ESP32-S3 is on SDA = GPIO16 and SCL = GPIO15.
  The carrier's own EEPROM answers on addresses 0x54–0x57 on the same bus.
- **Carrier board definition.** Do not use `board: esp32-s3-devkitc-1` for IoTsmart ESP32-S3.
  Use `variant: esp32s3`, `flash_size: 4MB` and `psram: mode: quad`, as in the configs here.

## 10. Verify Everything Is Working

- **Log.** `esphome logs <your-config>.yaml` shows the Wi-Fi connection, the API connection and, on start-up, an I2C scan
  (`scan: true`). The scan lists the modules on the HOST I2C bus.
- **Web page.** Open `http://<ip-address>/`. Switch an output and check the LED or load on the module.
- **Home Assistant.** The entities of the device respond to the switches and show the inputs.

## 11. Troubleshooting

| Problem | What to do |
|---|---|
| Serial port not listed or upload fails | Use another USB cable (some are charge-only). Put the chip in bootloader mode: hold BOOT, press and release RUN, release BOOT. |
| Build fails on Windows with a user name that contains a space | Set the environment variables `ESPHOME_ESP_IDF_PREFIX` and `ESPHOME_DATA_DIR` to paths without spaces. |
| Device does not join Wi-Fi | Check `secrets.yaml`. The network must be 2.4 GHz. Use the fallback access point (see step 7). |
| Device not found by name | Use the IP address from the log or from your router instead of `<name>.local`. |
| Output works the wrong way round | Check that `inverted: true` is still on the pin. The channels are active-low. |
