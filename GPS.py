import serial
import datetime
import os

from ublox_gps import UbloxGps

def main():
    port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
    gps = UbloxGps(port)

    # Acquires gps times and coordinates
    gps_times = []
    gps_coords = []
    try:
        print("Listening for UBX Messages")
        while True:
            try:
                time = datetime.now().second
                geo = gps.geo_coords()
                gps_times.append(time)
                gps_coords.append(geo)
                print("Longitude: ", geo.lon) 
                print("Latitude: ", geo.lat)
                print("Heading of Motion: ", geo.headMot)
            except (ValueError, IOError) as err:
                print(err)

    finally:
        export(gps_times, gps_coords)
        port.close()


def export(gps_times, gps_coords):
# Exports gps data to a csv
    logname = "gps.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    logfile.write("Times (s), Voltage (V)\n")
    for i in range(len(gps_times)):
        logfile.write(f"{gps_times[i]}, {gps_coords[i]:.7f}\n")
    logfile.close()    


if __name__ == '__main__':
    main()
