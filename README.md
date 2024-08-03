# NovelDownloader

## Project Overview

`NovelDownloader` is an application designed to download novels from a specific website. It provides a user-friendly interface where users can input a book ID to download the novel's content. The program supports pausing and resuming downloads and also offers interesting fun facts for entertainment.

## Features

*   **Download Novels**: Enter the book ID to download the novel content.
*   **Update Book Status**: Check if the book has new chapters available.
*   **Fun Facts**: Get random fun facts for entertainment.
*   **User Agreement**: Displays a user agreement at the start.

## Installation

### Prerequisites

*   Python 3.6 or higher
*   `pip` package manager

### Installing Dependencies

First, clone the project repository locally, then install the required packages:

```bash
git clone https://github.com/your_username/NovelDownloader.git
cd NovelDownloader
pip install -r requirements.txt
```


## Usage

### Starting the Application

After packaging, run the generated executable (e.g., `main.exe`) to start the application. Alternatively, in a development environment, you can directly run:

```css
python main.py
```

### How to Use

1.  After starting the application, a user agreement dialog will appear. Read the agreement and choose "Agree" or "Disagree."
2.  Enter the book ID and click the "Confirm" button to start the download.
3.  Click the "Update Book Status" button to check if there are new chapters available for the book.
4.  Click the "Get Fun Fact" button to receive a random fun fact.

### How to Obtain the Book ID

To obtain the book ID, navigate to the book's directory page on the website. For example, in the URL `https://fanqienovel.com/page/7216762831459665384`, the number `7216762831459665384` is the book ID. This ID is located at the end of the URL, following `/page/`.

## Project Structure

*   `main.py`: Main entry point of the application.
*   `download_utils.py`: Contains functions for downloading and decoding novel content.
*   `file_utils.py`: File operations such as saving and loading novel chapters.
*   `fun_facts.py`: Functions for fetching fun facts.
*   `agreement.py`: Manages the user agreement dialog and logic.
*   `setup.py`: Configuration file for packaging the application.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome contributions including but not limited to:

*   Bug fixes
*   New features
*   Documentation improvements

## Developer

*   **Peyjee**  
    GitHub: [Peyjee-W](https://github.com/Peyjee-W)

## License

This project is licensed under the MIT License. For more details, please refer to the LICENSE file.
