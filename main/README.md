# 使用センサー

- 水分センサー
- 温度センサー
- DOセンサー
- pHセンサー

### 水分センサー
https://www.amazon.co.jp/gp/product/B01GEZMRA0/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1

https://www.mysensors.org/build/light-lm393

### 温度センサー

- 温度計
https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf

- プローブ
https://www.amazon.co.jp/gp/product/B07M886SBK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1

### pHセンサー

- モジュール
https://www.diymore.cc/collections/ph-value-detect-sensor/products/diymore-liquid-ph-value-detection-detect-sensor-module-monitoring-control-for-arduino-m

- プローブ
https://www.diymore.cc/products/bnc-electrode-probe-connector-hydroponic-for-ph-aquarium-controller-meter-sensor

### D.Oセンサー

- キット
https://www.dfrobot.com/product-1628.html?search=do%20sensor&description=true

- 使い方
https://wiki.dfrobot.com/Gravity__Analog_Dissolved_Oxygen_Sensor_SKU_SEN0237#target_4



# 組み立て

- 水分センサー：GPIO -> 15(UART_RXD)
- 温度センサー：GPIO -> 4(GPCLK0)
- DOセンサー：ADS1115 -> A0
- pHセンサー：ADS1115 -> A1
