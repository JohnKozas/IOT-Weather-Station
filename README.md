# IoT-Weather-Station

An IoT weather station built using a Raspberry Pi that displays weather information on a local web page and on a smartphone using the Blynk IoT platform.

The code is entirely written in Python, covering both front-end and back-end development. It gathers sensor data from the Raspberry Pi and sends it to the Blynk IoT platform. The back-end 
consists of a PostgreSQL database running in a Docker container. Data is sent to the database using SQLAlchemy, and the database schema was created using DBeaver with SQL code. The 
front-end is a local web page built with Flask and Django, along with a simple HTML template to present the data.

The Raspberry Pi uses two sensors:
- **DFRobot BME280**: Measures temperature, atmospheric pressure, humidity, and altitude.
- **BH1750**: Measures light intensity.

  There is a PDF with a detailed step-by-step description of the implementation.
