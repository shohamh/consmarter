## Fridge Inventory Tracking App Design

**User Requirements:**

*   Create an app to track items in the fridge.
*   Easy to add and remove items.
*   Mechanisms:
    *   Camera: Identify objects, scan barcodes, read nutritional values and expiration dates.
    *   Manual Input: Slider for quantity, choose unit of measurement.
*   Local DB with optional sync for backups (privacy-conscious).
*   Data analysis: Consumption rates, shopping lists.
*   Deployment: Old Android phone next to fridge.
*   Accessible via browser.

**Technology Stack:**

*   **Front-end:** React Native.
*   **Back-end:** Python.

**Specific Requirements:**

1.  **Camera Integration:** The app should use the phone's camera to identify food items. It should also be able to scan barcodes to retrieve product information. The camera should only be activated when necessary to preserve privacy.
2.  **Manual Input:** Users should be able to manually add and remove items, specifying the quantity and unit of measurement (e.g., 50%, 200 grams).
3.  **Local Database:** The app should store the inventory data in a local database on the phone. There should be an option to sync the data to a remote location for backup purposes.
4.  **Data Analysis:** The app should provide data analysis features, such as consumption rates for different items and automatic shopping list generation.
5.  **Deployment:** The app should be deployable on an old Android phone and accessible via a web browser for development and analysis.

**Task:**

Create a step-by-step plan for designing and developing this application using React Native for the front-end and Python for the back-end.