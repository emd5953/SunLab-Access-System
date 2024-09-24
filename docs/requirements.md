# SUN Lab Access System

## Project Overview
The **SUN Lab Access System** is designed to track and manage access to the Student Unix Network (SUN) Lab. The system records the entry and exit of students using their student IDs and timestamps. It also provides authorized administrators with the ability to browse and search these records through a graphical user interface (GUI).

## High-Level Requirements

### Functional Requirements
1. **Database Storage**:
   - The system **must** store student ID numbers and timestamps for lab access (entry/exit).
   - Records **must** be stored for 5 years.

2. **Card Reader Interface**:
   - The system **must** capture student ID and timestamps from a card reader device when a student enters or exits the lab.

3. **GUI for Admins**:
   - An admin GUI **must** allow authorized personnel to browse and search the access history.
   - Search filters **must** include:
     - Date
     - Student ID
     - Time range

4. **Authorization**:
   - Only authorized personnel **must** be allowed to access and manage the records.

5. **Future Extensions**:
   - The system **must** support additional user types such as students, faculty, staff, and janitors.
   - Admins **must** be able to activate, suspend, and reactivate user IDs.

### Non-Functional Requirements
1. **Reliability**:
   - The system **shall** be operational 24/7 for uninterrupted lab access.

2. **Scalability**:
   - The system **shall** be scalable to support more users and potentially more lab locations.

3. **Security**:
   - The system **must** securely store and transmit sensitive data (student IDs and timestamps).
   - Only authorized users **must** have access to sensitive information.

4. **Maintainability**:
   - The system **must** be maintainable and easy to extend with future functionalities.

## Technology Stack
- **Programming Language**: Python 3
- **Database**: Firebase (NoSQL)
- **GUI Framework**: TBD (suggesting `Tkinter`, `PyQt`, or `Kivy`)
- **Version Control**: Git

## Instructions to Run the Project
(TBD: Add instructions for setting up the environment, running the code, etc.)

## Future Work
- Add support for different user types (faculty, staff, janitors).
- Implement user account activation, suspension, and reactivation.

## Repository Structure
