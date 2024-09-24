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

The logData collection serves as the logbook for all access attempts to the SUN Lab. Each entry in this collection is mapped to a specific user by their unique ID and contains information about the date and time of access attempts. This collection is critical for maintaining an audit trail and can be used by administrators to monitor lab access.

Fields:
ID: The same unique identifier used in the labAccess collection to map access logs to a specific user (e.g., 256898679).
datetime: A timestamp in ISO 8601 format that records the exact date and time when the user attempted to access the lab. This helps in tracking the access history over time.
name: The name of the individual attempting to access the lab. This field is redundant with the labAccess collection but is useful for quick access without cross-referencing.

#### Example:
```json

"256898679": {
  "datetime": "2023-09-22T14:23:45Z",
  "name": "William Turner"
}
Current Data Example:
In the current dataset provided, the datetime fields are empty, indicating that access attempts have not yet been logged:

'''json:

"256898679": {
  "datetime": "",
  "name": "William Turner"
}



Database Structure Summary
labAccess:
Field	Type	Description
ID	String	Unique user ID (e.g., student ID or faculty ID).
access	String	Whether the user has access to the lab ("true", "false").
affiliation	String	The role of the user, either "faculty" or "student".
name	String	Full name of the user.
logData:
Field	Type	Description
ID	String	Unique user ID (same as in labAccess).
datetime	String	Date and time of the access attempt (ISO 8601 format).
name	String	Full name of the user.
