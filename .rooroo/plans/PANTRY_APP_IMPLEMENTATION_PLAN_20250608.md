# Pantry App Implementation Plan (Updated)

## Parent Task ID
`ROO#PANTRY_APP_202506082130`

## Overall Strategy
Build in 3 phases with updated tech stack:
1. **MVP (4 weeks)**: Core functionality with local-first approach
2. **V1 (3 weeks)**: Voice integration + shopping lists
3. **V2 (5 weeks)**: Image recognition + analytics

### Revised Tech Stack
| Component | Technology | Justification |
|-----------|------------|---------------|
| **Frontend** | React Native + Expo | Cross-platform, optimized for mobile |
| **Backend** | Python + FastAPI | Simple, high-performance API |
| **Database** | SQLite (local) | Zero-config, no cloud dependency |
| **Barcode** | ZXing (React Native port) | Open-source, mobile-optimized |
| **Voice** | Expo Speech API | Built-in, free solution |
| **Notifications** | Expo Notifications | Native push notifications |
| **Image Rec** | TensorFlow Lite | Mobile-optimized ML |

## Phase 1: MVP Implementation (4 weeks)
### Sub-tasks
1. **Project Setup** (`ROO#SUB_MVP_SETUP_20250608A`)
   - Create Expo project
   - Setup FastAPI backend
   - Initialize SQLite database
   - *Expert: Developer*

2. **Barcode Integration** (`ROO#SUB_MVP_BARCODE_20250608B`)
   - Integrate ZXing React Native
   - Local product database (OpenFoodFacts)
   - *Expert: Developer*

3. **Inventory Core** (`ROO#SUB_MVP_INVENTORY_20250608C`)
   - Item CRUD operations
   - Expiry tracking system
   - Location management
   - *Expert: Developer*

4. **Dashboard & Alerts** (`ROO#SUB_MVP_UI_20250608D`)
   - Inventory visualization
   - Expiry alert system
   - Expo notification setup
   - *Expert: Developer*

## Phase 2: V1 Enhancements (3 weeks)
### Sub-tasks
1. **Voice Integration** (`ROO#SUB_V1_VOICE_20250608E`)
   - Expo Speech API implementation
   - Command parser ("Used 2 eggs")
   - *Expert: Developer*

2. **Shopping List** (`ROO#SUB_V1_SHOPPING_20250608F`)
   - Auto-list generation logic
   - Consumption pattern analysis
   - *Expert: Developer + Analyzer*

## Phase 3: V2 Advanced Features (5 weeks)
### Sub-tasks
1. **Image Recognition** (`ROO#SUB_V2_VISION_20250608G`)
   - TensorFlow Lite model training
   - Produce recognition (fruits/veggies)
   - *Expert: Developer*

2. **Analytics Engine** (`ROO#SUB_V2_ANALYTICS_20250608H`)
   - Consumption heatmaps
   - Waste reduction reports
   - *Expert: Analyzer*

3. **Optimization** (`ROO#SUB_V2_PERF_20250608I`)
   - React Native performance tuning
   - Offline capability enhancements
   - *Expert: Developer*

## Key Changes from Original
- Frontend: React Native + Expo instead of Preact
- Backend: Python + FastAPI instead of Node.js
- Voice: Expo Speech API instead of Web Speech API
- Image Recognition: TensorFlow Lite instead of TensorFlow.js
- Notifications: Expo Notifications instead of PWA

## Updated Assumptions
1. Local-first approach maintained
2. React Native works on target device (old Android phone)
3. Expo provides adequate performance