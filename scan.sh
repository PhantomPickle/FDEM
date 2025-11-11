echo "Enter scan duration:"
read USERVAL
aplay ~/Documents/FDEM/output_waveform_pure.wav \
& sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/signal_acquisition.py "$USERVAL" \
& sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/gps.py "$USERVAL"
rclone copy ~/Documents/FDEM/data onedrive:Documents/Academic/Coding/FDEM/data
echo CSVs copied to OneDrive.
