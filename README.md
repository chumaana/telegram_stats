# **Telegram Chat Statistics**

This program is designed to analyze Telegram chat data using the Telegram API and Python libraries. It provides statistics and insights into chat interaction and displays it using Tkinter

## **Functionality**

- The program requests messages from the selected chat and stores them in a database.
- It displays various statistics based on the collected data, such as the total number of messages, message types, user-specific data, etc.
- Users can input a time period to view statistics for that specific duration.
- Upon termination of the program, all database tables are cleared, maintaining user session data for future access without re-authentication.

## **Getting Started**

### **Prerequisites**

- Obtain your api_hash and api_id from the Telegram API. Add these details to the `config.ini` file. An example configuration file is available in `config_example`.
- Ensure you have the following installed:

  - **Tkinter** for GUI (Graphical User Interface)

    ```bash
    apt-get install python3-tk
    ```

  - **Bootstrap** for Tkinter

    ```bash
    pip3 install ttkbootstrap
    ```

  - **Telethon** for Telegram API interaction

    ```bash
    pip install telethon
    ```

## **Usage**

- Clone the repository to your local machine.
- Navigate to the root directory of the project.
- Run the following command in your terminal:

  ```bash
  python3 main.py
  ```
