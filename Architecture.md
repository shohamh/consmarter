# Smart Fridge App Architecture

## Overview
A privacy-focused cross-platform application (Android + Web) for fridge inventory management using local processing, multiple identification methods, and sensor integration. The app tracks items via camera, barcode scanning, and user input, with support for various quantity units and expiration dates to minimize food waste.

## Core Components
1. **Multi-Platform GUI**
   - Built with React Native for unified Android/web interface
   - Responsive design for phone and web browser display
   - Real-time inventory dashboard with quantity sliders

2. **Camera Module**
   - Activated manually or via motion sensor trigger
   - Captures items with optional auto-capture on motion detection
   - Uses TensorFlow Lite for on-device ML processing

3. **Barcode Scanner**
   - Integrated with Zebra Technologies' on-device scanning SDK
   - Supports manual override for item name/quantity
   - Works offline with local barcode database

4. **Image Recognition Engine**
   - Local object detection using MobileNetV2 models
   - Cross-references items with existing database for faster recognition
   - Supports multiple quantity units: whole, liters, grams, percentage

5. **Local Database (Room Persistence Library)**
   - Stores item metadata: name, quantity (with unit), expiration date
   - Maintains user-defined thresholds and historical usage patterns
   - Encrypted with SQLCipher for security

6. **Sensor Integration**
   - Optional weight sensors in fridge compartments
   - Motion detection to trigger camera capture
   - Door open/close sensor for usage pattern analysis

7. **Notification System**
   - Local alarms for expiration warnings
   - Quantity threshold alerts
   - No cloud-based tracking

8. **Shopping List Generator**
   - Calculates needed items based on:
     - Expiration dates
     - Current quantities
     - User-defined minimum thresholds
   - Exports JSON for manual use

## Data Flow
```mermaid
graph TD
    A[User Activates Camera] --> B[Image Captured]
    B --> C[Local ML Processing]
    C --> D[Item Identified]
    D --> E[Update Database]
    E --> F[UI Refresh]
    F --> G[User Adjusts Quantity]
    G --> H[Update Database]
    H --> I[Shopping List Generator]
    I --> J[Output Shopping List]
    K[Barcode Scan] --> L[Database Lookup]
    L --> M[Update Item Quantity]
    N[Motion Sensor] --> O[Camera Activation Prompt]
    O --> P[Capture on User Consent]