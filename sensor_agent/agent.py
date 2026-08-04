import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import httpx

API_URL = "http://127.0.0.1:8000/api/v1/measurements"
INTERVAL_SECONDS = 60


def init_bme280():
    """Initialize I2C bus and BME280 sensor instance."""
    i2c = board.I2C()
    sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

    return sensor


def main():
    """Main execution loop reading sensor data and sending it to API."""
    print("Starting BME280 measurement agent...")

    try:
        sensor = init_bme280()
        print("BME280 sensor detected successfully.")
    except Exception as e:
        print(f"Sensor initialization error: {e}")
        return

    with httpx.Client(timeout=10.0) as client:
        while True:
            try:
                temperature = round(sensor.temperature, 2)
                humidity = round(sensor.relative_humidity, 2)
                pressure = round(sensor.pressure, 2)

                payload = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "pressure": pressure,
                }

                response = client.post(API_URL, json=payload)
                response.raise_for_status()

                print(f"Measurement sent: T={temperature}°C, H={humidity}%, P={pressure}hPa")

            except httpx.RequestError as exc:
                print(f"API connection error: {exc}")
            except httpx.HTTPStatusError as exc:
                print(f"Server returned HTTP error {exc.response.status_code}: {exc.response.text}")
            except Exception as e:
                print(f"Unexpected sensor reading error: {e}")

            time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()