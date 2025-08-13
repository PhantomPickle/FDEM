aplay ~/Documents/FDEM/output_waveform_chirp.wav & sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/signal_acquisition.py & sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/gps.py
rclone copy ~/Documents/FDEM/data onedrive:Documents/Academic/Coding/FDEM/data
echo CSVs copied to OneDrive.