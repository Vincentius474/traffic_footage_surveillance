# TrafficVision

## Traffic Footage Surveillance & Inspection System

Traffic Footage Surveillance is a Python-based computer vision application designed to analyze traffic footage, detect and track vehicles, identify license plates, perform OCR, capture vehicle evidence, and provide an interactive interface for inspecting traffic events.

The system combines **YOLO object detection and tracking**, **license plate detection**, **OCR**, **OpenCV video processing**, and a **Tkinter desktop interface** into a single traffic footage analysis tool.

---
<img width="1915" height="1079" alt="Screenshot 2026-09-30 002514" src="https://github.com/user-attachments/assets/4c054416-b832-4ff3-88e8-e7f80b8c6e61" />


## Features

### Vehicle Detection & Tracking
- Detects cars, motorcycles, buses, and trucks.
- Uses YOLO for object detection.
- Assigns tracking IDs to detected vehicles.
- Displays vehicle bounding boxes and confidence scores.
- Maintains vehicle information while the vehicle is visible.

### Traffic Event Detection
- Configurable virtual counting line.
- Detects when tracked vehicles cross the counting line.
- Records vehicle direction.
- Prevents repeated capture of the same tracked vehicle.

### Vehicle Capture
When a vehicle event is detected, TrafficVision can capture:
- Vehicle image
- Vehicle type
- Tracking ID
- Detection confidence
- Direction
- Timestamp

Captured vehicle images are stored in:

```text
output/vehicles/
```

### License Plate Detection
For captured vehicles, the application:
1. Extracts the vehicle region.
2. Runs a dedicated license plate detection model.
3. Selects a detected plate.
4. Saves the plate image.

Plate images are stored in:

```text
output/plates/
```

### License Plate OCR
TrafficVision uses EasyOCR to extract text from detected license plates.

The system records:
- Plate number
- OCR confidence
- Plate image

If OCR cannot read the plate, the event is still retained and the plate image can be saved for later inspection.

### Vehicle Inspector
The Vehicle Inspector displays:
- Vehicle ID
- Vehicle type
- Detection confidence
- Direction
- License plate
- Plate confidence
- Timestamp
- Captured vehicle image
- Captured license plate image

The inspector includes a vertical scrollbar so all information remains accessible when the application window is smaller than the inspector contents.

### Video Playback & Inspection
Available controls include:
- Open video
- Play
- Pause
- Previous frame
- Next frame
- Rewind
- Fast forward
- Playback speed control
- Zoom in
- Zoom out
- Reset zoom
- Mouse-wheel zoom
- Video panning
- Timeline navigation

### AI Detection Toggle
AI detection can be enabled or disabled during inspection.

### Vehicle Event Table
The application maintains a table containing detected and captured vehicles with:
- ID
- Type
- Plate
- Direction
- Confidence
- Timestamp

Selecting a vehicle updates the Vehicle Inspector.

### CSV Reporting
Traffic events are stored in:

```text
output/reports/traffic_events.csv
```

The report contains fields including:

```text
event_id
timestamp
vehicle_id
vehicle_type
direction
confidence
plate_number
plate_confidence
vehicle_image
plate_image
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| OpenCV | Video processing and image manipulation |
| Ultralytics YOLO | Vehicle detection and tracking |
| EasyOCR | License plate text recognition |
| Tkinter | Desktop graphical user interface |
| Pillow | Image handling inside Tkinter |
| CSV | Traffic event reporting |

---

## Project Structure

```text
traffic_vehicle_counter/
│
├── main.py
│
├── core/
│   ├── __init__.py
│   ├── tracker.py
│   ├── counter.py
│   ├── plate_detector.py
│   ├── plate_reader.py
│   ├── capture_manager.py
│   └── video_manager.py
│
├── gui/
│   ├── __init__.py
│   ├── application.py
│   ├── video_panel.py
│   ├── control_panel.py
│   ├── vehicle_panel.py
│   └── vehicle_table.py
│
├── models/
│   ├── yolov8n.pt
│   └── license-plate-finetune-v1n.pt
│
├── input/
│
└── output/
    ├── vehicles/
    ├── plates/
    ├── frames/
    ├── videos/
    └── reports/
        └── traffic_events.csv
```

---

## How the System Works

```text
Traffic Video
      │
      ▼
Video Manager
      │
      ▼
YOLO Vehicle Detection
      │
      ▼
Vehicle Tracking
      │
      ▼
Counting Line / Traffic Event
      │
      ▼
Vehicle Capture
      │
      ▼
Vehicle Crop
      │
      ▼
License Plate Detection
      │
      ▼
License Plate Crop
      │
      ▼
EasyOCR
      │
      ▼
Vehicle + Plate Evidence
      │
      ├── Vehicle Image
      ├── Plate Image
      └── CSV Report
```

---

## Requirements

Recommended environment:

- Python 3.12+
- Windows, Linux, or macOS
- At least 8 GB RAM recommended
- GPU is optional

Python dependencies:

```text
opencv-python
ultralytics
pillow
easyocr
```

Ultralytics tracking may also require the `lap` package depending on the installed environment.

---

## Installation

### 1. Clone the project

```bash
git clone <your-repository-url>
cd traffic_vehicle_counter
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install opencv-python ultralytics pillow easyocr
```

If required by the tracking environment:

```bash
pip install lap
```

### 4. Add the YOLO models

Place the required models inside:

```text
models/
```

For example:

```text
models/yolov8n.pt
models/license-plate-finetune-v1n.pt
```

Make sure the model paths used by the application match the actual filenames.

---

## Running the Application

Activate the virtual environment and run:

```bash
python main.py
```

Click **Open Video** and select a traffic footage file.

Common supported formats include:

```text
.mp4
.avi
.mkv
.mov
```

Actual support depends on the OpenCV codecs available on the system.

---

## Using TrafficVision

### Step 1 — Open a Video

Click **Open Video** and select a traffic footage file.

### Step 2 — Start Playback

Use **Play** to start playback.

### Step 3 — Enable AI Detection

When AI detection is enabled, vehicles are detected and tracked automatically.

### Step 4 — Monitor Vehicle Events

Vehicles crossing the configured counting line can trigger a capture event.

### Step 5 — Inspect a Vehicle

Select a vehicle from the vehicle table. The Vehicle Inspector displays the selected vehicle's information and captured evidence.

### Step 6 — Review Images

The inspector provides captured vehicle and license plate images.

### Step 7 — Review the CSV Report

Traffic events are saved to:

```text
output/reports/traffic_events.csv
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Space` | Play / Pause |
| `Left Arrow` | Previous frame |
| `Right Arrow` | Next frame |
| `Ctrl + O` | Open video |

---

## Zoom & Navigation

The video viewer uses a fixed viewport so zooming does not resize the application controls.

Available controls include:
- Zoom in
- Zoom out
- Reset zoom
- Mouse-wheel zoom
- Click-and-drag panning

---

## Output Files

### Vehicle Images

```text
output/vehicles/
```

Example:

```text
vehicle_00001_car.jpg
vehicle_00002_truck.jpg
```

### License Plate Images

```text
output/plates/
```

Example:

```text
plate_00001.jpg
plate_00002.jpg
```

### Traffic Report

```text
output/reports/traffic_events.csv
```

---

## Example Event

```text
Event ID:             00015
Vehicle ID:           7
Vehicle Type:         Car
Direction:            DOWN
Detection Confidence: 94.2%
Plate:                ABC123
Plate Confidence:     88.6%
Timestamp:            2026-09-30 10:42:18
```

The corresponding vehicle and plate images are stored in the output directories.

---

## Design Architecture

TrafficVision separates the application into core processing components and GUI components.

### Core Layer

```text
VideoManager
     │
     ├── Reads video
     ├── Tracks frame position
     └── Handles seeking

VehicleTracker
     │
     ├── YOLO detection
     ├── Vehicle classification
     └── Object tracking

PlateDetector
     │
     └── License plate detection

PlateReader
     │
     └── OCR processing

CaptureManager
     │
     ├── Saves vehicle images
     ├── Saves plate images
     └── Writes CSV events
```

### GUI Layer

```text
Application
    │
    ├── VideoPanel
    ├── ControlPanel
    ├── VehicleTable
    └── VehiclePanel
```

This separation makes the application easier to maintain and extend.

---

## Vehicle Classes

The application currently supports:

```python
VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}
```

Tracker confidence can be configured:

```python
VehicleTracker(
    model_path="models/yolov8n.pt",
    confidence=0.5
)
```

License plate detection confidence can also be configured:

```python
PlateDetector(
    model_path="models/license-plate-finetune-v1n.pt",
    confidence=0.25
)
```

---

## Current Development Status

- [x] Video file selection
- [x] Video playback
- [x] Pause/resume
- [x] Frame-by-frame navigation
- [x] Rewind
- [x] Fast forward
- [x] Playback speed control
- [x] Zoom and pan
- [x] YOLO vehicle detection
- [x] Vehicle tracking
- [x] Vehicle classification
- [x] Counting line
- [x] Vehicle event capture
- [x] Vehicle image capture
- [x] License plate detection
- [x] License plate image capture
- [x] License plate OCR
- [x] Vehicle Inspector
- [x] Scrollable inspector panel
- [x] Vehicle event table
- [x] CSV event reporting
- [x] AI detection toggle

---

## Planned Enhancements

- [ ] Multi-frame / best-frame vehicle selection
- [ ] Multi-frame license plate selection
- [ ] Improved OCR preprocessing
- [ ] Separate plate detection and OCR confidence values
- [ ] Search and filtering of captured vehicles
- [ ] Vehicle statistics dashboard
- [ ] Vehicle type counters
- [ ] Directional traffic statistics
- [ ] FPS monitoring
- [ ] Configurable counting line using the mouse
- [ ] Confidence threshold controls
- [ ] Full-frame evidence capture
- [ ] Annotated video export
- [ ] Event timeline and bookmarks
- [ ] Manual vehicle and plate capture
- [ ] Background OCR processing
- [ ] GPU acceleration
- [ ] Application settings panel
- [ ] Session-based output folders
- [ ] PDF traffic reports
- [ ] PyInstaller executable packaging

---

## Performance Considerations

Vehicle detection, tracking, plate detection, and OCR can be computationally expensive.

For better performance:
- Use a GPU-enabled environment where appropriate.
- Use a smaller YOLO model for faster inference.
- Avoid running OCR on every frame.
- Process license plates only when a relevant vehicle event occurs.
- Keep captured frame history limited.
- Move expensive OCR operations to background workers as the application grows.

---

## Responsible Use

TrafficVision is intended as a computer vision and traffic-footage analysis project.

When using real-world footage containing identifiable vehicles or license plates, users should ensure that they have appropriate authorization and comply with applicable privacy, data-protection, and surveillance requirements.

---

## Project Goals

This project demonstrates practical skills in:

- Computer vision
- Object detection
- Object tracking
- Image processing
- OCR
- Video analytics
- Python software engineering
- GUI development
- Data collection
- CSV reporting
- Modular application architecture

It demonstrates how machine learning models can be integrated into a complete desktop software application.

---

## License

Add the license that applies to this project and its dependencies.

Individual machine-learning models may have their own licenses and usage requirements. Check the license of each model before distributing or deploying the application.

---

## Author

**Reatlehile Vincent Sello**

Aspiring Data & ML Engineer

This project demonstrates the integration of machine learning, computer vision, software engineering, and data analytics into an end-to-end application.
