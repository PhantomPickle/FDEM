cleanup() {
    echo "Caught interrupt, terminating processes..."
    kill $(jobs -p)
    exit 0
}

trap cleanup SIGINT

echo "Enter scan duration:"
read USERVAL

aplay ~/Documents/FDEM/output_waveform_pure.wav &
sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/signal_acquisition.py "$USERVAL" &
sudo ~/Documents/FDEM_venv/bin/python ~/Documents/FDEM/gps.py "$USERVAL" &

# Wait for all background processes to complete
wait

rclone copy ~/Documents/FDEM/data onedrive:Documents/Academic/Coding/FDEM/data
echo CSVs copied to OneDrive.
