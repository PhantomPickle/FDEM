echo "Enter scan duration:"
read USERVAL
sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/button_mag.py "$USERVAL" \
& sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/gps.py "$USERVAL"
rclone copy ~/Documents/FDEM/data onedrive:Documents/Academic/Coding/FDEM/data
echo CSVs copied to OneDrive.
