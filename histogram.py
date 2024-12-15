import argparse
import re
from collections import Counter
from tqdm import tqdm  
from colorama import init, Fore

# Inicjalizacja koloro - po każdym użyciu funkcji kolorowania, kolor zostanie zresetowany do domyślnego
init(autoreset=True)

def process_file(filename, min_length=0):
    """Process the file to count word frequencies."""
    word_counter = Counter()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines first to get total count for the progress bar
            for line in tqdm(lines, desc=f"Processing {filename}", unit="line"):  # Line-wise progress
                # Split line into words and clean them
                words = re.findall(r'\b\w+\b', line.lower())
                filtered_words = [word for word in words if len(word) >= min_length]
                word_counter.update(filtered_words)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    return word_counter

def display_word_list(word_counts, limit):
    """Displays words sorted by frequency."""
    print(f"\nTop {limit} words by frequency:\n")
    for word, count in word_counts.most_common(limit):
        print(f"{word}: {count}")

def get_color_for_frequency(count, max_count):
    """Returns a color based on the frequency of the word."""
    # We can map frequencies to a gradient of colors
    # For this we use the count value compared to the max_count
    percentage = count / max_count
    if percentage > 0.75:
        return Fore.GREEN  # High frequency - green
    elif percentage > 0.5:
        return Fore.YELLOW  # Medium-high frequency - yellow
    elif percentage > 0.25:
        return Fore.CYAN  # Medium frequency - cyan
    else:
        return Fore.RED  # Low frequency - red

def print_histogram(word_counts, limit):
    """Prints a colored ASCII histogram with horizontal rectangles of the top 'limit' words by frequency."""
    # Get the most common words and their counts
    common_words = word_counts.most_common(limit)
    max_count = common_words[0][1] if common_words else 1  # Avoid division by 0

    # Width of the rectangle
    max_bar_width = 50  # Max width for the largest count

    print(f"\nTop {limit} Words Histogram (Colored ASCII Rectangles in Horizontal):")

    for word, count in common_words:
        # Scale the bar length based on the count
        bar_length = int(count / max_count * max_bar_width)
        bar = f"{'█' * bar_length}"
        # Get the color for the word based on its frequency
        color = get_color_for_frequency(count, max_count)
        print(f"{color}{word: <15} | {bar} {count}")

def main():
    parser = argparse.ArgumentParser(description="List words by frequency from a text file.")
    parser.add_argument('filename', help='Path to the text file to process.')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Number of words to display (default: 10).')
    parser.add_argument('--min-length', '-m', type=int, default=0, help='Minimum length of words to include (default: 0).')
    args = parser.parse_args()

    # Process the file
    word_counts = process_file(args.filename, min_length=args.min_length)

    # Display the word list
    display_word_list(word_counts, args.limit)

    # Print the colored ASCII histogram with true rectangles
    print_histogram(word_counts, args.limit)

if __name__ == '__main__':
    main()

    # Biblioteki
    # argparse - opcje programu np. zmiana liczby, dlugosci wyświetlanych słów
    # re - wyodrebnia slowa z text.txt
    # counter - zliczanie elementow w iterowalnym obiekcie = lista, liczenie częstotliwości występowania słów w tekście
    # tqdm - wyświetlanie paska postępu w konsoli, postęp przetwarzania zbiorów danych (plików lub list)
    # colorama - kolorowanie tekstu w terminalu, używana do kolorowania słów na podstawie ich częstotliwości w histogramie
    