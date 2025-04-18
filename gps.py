import serial
from datetime import datetime as date
import os
from ublox_gps import UbloxGps

def main():
    
    port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
    gps = UbloxGps(port)

    scan_duration = 2 # In [s]
    gps_rate = 1 # In [Hz] determined by testing-- how to set this?
    num_samples = scan_duration*gps_rate
    
    # Acquires gps times and coordinates
    gps_times = []
    gps_lat = []
    gps_lon = []
    gps_head = []
    try:
        print("Recording GPS Coordinates")
        start_time = date.now().timestamp()
        print(start_time)
        time = 0
        while time < num_samples: # Only works because gps_rate is currently 1 Hz
            try:
                time = date.now().timestamp() - start_time
                print(time)
                geo = gps.geo_coords()
                gps_times.append(time)
                gps_lat.append(geo.lat)
                gps_lon.append(geo.lon)
                gps_head.append(geo.headMot)
                print(f'Lat: {gps_lat:.2f}, Lon: {gps_lon:.2f}\n')
            except (ValueError, IOError) as err:
                print(err)
        gps_times = gps_times + start_time
    finally:
        export(gps_times, gps_lat, gps_lon, gps_head)
        port.close()


def export(gps_times, gps_lat, gps_lon, gps_head):
# Exports gps data to a csv
    logname = "gps.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    logfile.write("Times (s),Latitude,Longitude,Heading\n")
    print("Writing gps data to log file.")
    for i in range(len(gps_times)):
        logfile.write(f"{gps_times[i]},{gps_lat[i]:.7f}, {gps_lon[i]:.7f}, {gps_head[i]:.7f}\n")
    logfile.close()    


if __name__ == '__main__':
    main()
