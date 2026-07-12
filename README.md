# Navenie-AMS-PRJ
ICONIC UNIVERSITY PROJECT CAPSTONE

# NAVENIE AMS (Academic Management System)

![NAVENIE AMS](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

**NAVENIE AMS (Academic Management System)** is a professional offline standalone school management solution developed to simplify academic administration in primary, secondary, and tertiary educational institutions. The system enables schools to efficiently manage student records, examination results, user accounts, and generate printable reports while maintaining a secure local SQLite database.

The project also includes a **Parent Result Checking Portal**, a Flask-powered web application that allows parents and guardians to securely access students' academic results through a web browser.

---

# Components

## 1. NAVENIE_AMS_Setup.exe

The offline desktop application designed for school administrators, examination officers, teachers, and bursars.

### Features

* Student Registration
* Student Record Management
* Examination Result Entry
* Continuous Assessment Management
* Automatic Grade Computation
* Student Search
* Class Management
* Academic Session Management
* PDF Result Printing
* Excel Export
* User Authentication
* Local SQLite Database
* Secure Offline Operation
* Backup & Restore Support

---

## 2. NAVENIE AMS.exe (Parent Result Checking Portal)

A Flask-powered web application that enables parents and guardians to securely access students' examination results through a web browser.

### Features

* Secure Parent Login
* Student Information Display
* Academic Session Selection
* Academic Term Selection
* View Examination Results
* Download / Print Result Sheet
* Responsive User Interface
* Direct Connection to NAVENIE AMS Database
* Session-Based Authentication

---

# Technologies Used

* Python
* Tkinter
* Flask
* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* SQLite3
* ReportLab
* OpenPyXL
* PyInstaller
* Inno Setup Compiler

---

# Project Structure

```text
NAVENIE AMS
│
├── NAVENIE_AMS_Setup.exe
│
├── Parent Result Portal
│     ├── NAVENIE AMS.exe
│     ├── backend
│     ├── templates
│     ├── static
│     └── school.db
│
└── Database
      school.db
```

---

# Parent Result Portal

The Parent Result Portal retrieves student records directly from the NAVENIE AMS SQLite database.

Parents authenticate using:

* **Username:** Student Full Name
* **Password:** Admission Number

After successful login, parents can:

* View Student Information
* Select Academic Session
* Select Academic Term
* View Examination Results
* Download or Print Result Sheets

---

# Running the Parent Result Portal

## Important Notice

> **The Flask server must be running before the Parent Result Portal can be accessed.**

Start the Flask backend by running:

```bash
py backend/"NAVENIE AMS.py"
```

or by launching:

```text
NAVENIE AMS.exe
```

Once the Flask server is running, open your web browser and navigate to:

```text
http://127.0.0.1:5000
```

The Parent Result Checking Portal login page will be displayed.

---

# System Requirements

* Windows 10 / Windows 11
* Python 3.10 or later (Development Environment)
* Modern Web Browser (Chrome, Edge, Firefox, etc.)
* SQLite Database

---

# Default Database Location

```text
%APPDATA%\NAVENIE AMS\school.db
```

The Parent Result Portal automatically connects to the existing NAVENIE AMS database.

---

# Installation

## Offline Desktop Application

Run:

```text
NAVENIE_AMS_Setup.exe
```

Follow the installation wizard to install NAVENIE AMS.

## Parent Result Portal

Launch:

```text
NAVENIE AMS.exe
```

This starts the Flask backend server. After the server starts successfully, open:

```text
http://127.0.0.1:5000
```

or allow the application to automatically launch your default web browser if configured.

---

# Security Features

* Secure Login Authentication
* Session-Based Authentication
* Protected Dashboard Access
* Secure Local SQLite Database
* Unauthorized Access Prevention

---

# Future Enhancements

* Cloud Database Integration (Supabase/PostgreSQL)
* Online Synchronization
* SMS Notification System
* Email Notification System
* Student Portal
* Teacher Portal
* Parent Portal Enhancements
* Bursary & Finance Module
* Mobile Application
* Online Payment Integration
* Multi-School Management
* Cloud Backup & Restore

---

# Developer

## **ANGEL NAITBJ**

### **(NORBERT APRIL IGWE THEO BAR-JEHOSHUA ANGEL)**

**Founder, Software Engineer & System Architect**

**NAVENIE Technologies**

Developer of the **NAVENIE Academic Management System (NAVENIE AMS)** and the **Parent Result Checking Portal**, focused on building innovative educational technologies that enhance school administration, academic management, and digital transformation within educational institutions.

---

# License

This project is released under the **MIT License**.

---

# Acknowledgements

Special appreciation to all contributors, testers, educational institutions, and users whose feedback and support have contributed to the continuous development and improvement of the NAVENIE Academic Management System.

---

## ⭐ Support the Project

If you find this project useful, please consider giving it a **⭐ Star** on GitHub and sharing it with others.

Your support helps improve the project and encourages continued development of innovative educational software solutions.

