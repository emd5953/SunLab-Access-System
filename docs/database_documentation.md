# Firebase Database Documentation

## Overview
This document provides the details of the Firebase database structure used for the SUN Lab access system. The database contains two main collections: `labAccess` and `logData`.

### 1. labAccess

This collection stores information about users who have access to the lab. Each entry represents a user identified by a unique ID, with the following fields:

- **ID**: The unique identifier for each user (e.g., `256898679`).
- **access**: A boolean-like string (`"true"` or `"false"`) indicating whether the user has access.
- **affiliation**: The user’s role (e.g., `"faculty"` or `"student"`).
- **name**: The name of the individual.

#### Example:
```json
"256898679": {
  "access": "true",
  "affiliation": "faculty",
  "name": "William Turner"
}

### 2. logData

The logData collection serves as the logbook for all access attempts to the SUN Lab. Each entry in this collection is mapped to a specific user by their unique ID and contains information about the date and time of access attempts.

Fields:

ID:        The same unique identifier used in the labAccess collection to map access logs to a specific user.
datetime:  A timestamp that records the exact date and time when the user attempted to access the lab.
name:      The name of the individual attempting to access the lab.


#### json Example:
"256898679": {
  "datetime": "2023-09-22T14:23:45Z",
  "name": "William Turner"
}

Current Data json Example:
In the current dataset provided, the datetime fields are empty, indicating that access attempts have not yet been logged:
"256898679": {
  "datetime": "",
  "name": "William Turner"
}