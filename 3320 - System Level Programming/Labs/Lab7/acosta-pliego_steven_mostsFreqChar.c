#include <stdio.h>
#include <ctype.h>
#include <fcntl.h>
#include <unistd.h>

#define FILENAME "sample.txt"
#define BUFFER_SIZE 1024  // Buffer size for reading the file

int main() {
    int fd;
    int freq[26] = {0};  // 26 letters
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead;
    char ch;
    
    //Opens the file
    fd = open(FILENAME, O_RDONLY);
    printf("Opening %s.\n", FILENAME);
    
    //Base case
    if (fd == -1) {
        perror("Error");
        return 1;
    }

    //Reads from the file in chunks
    while ((bytesRead = read(fd, buffer, BUFFER_SIZE)) > 0) {
        for (ssize_t i = 0; i < bytesRead; i++) {
            ch = buffer[i];
            if (isalpha(ch)) {  //checks if the char is alphabetic
                ch = tolower(ch);  //converts to lowercase
                freq[ch - 'a']++;  //adds the frequency
            }
        }
    }

    //another base case
    if (bytesRead == -1) {
        perror("Error");
        close(fd);  //close the file if error
        return 1;
    }

    close(fd);  //closes the file

    //finds the msot frequent character with linear search
    int maxFreq = 0;
    char mostFrequentChar = '\0';
    for (int i = 0; i < 26; i++) {
        if (freq[i] > maxFreq) {
            maxFreq = freq[i];
            mostFrequentChar = i + 'a';
        }
    }

    //prints the results
    if (maxFreq > 0) {
        printf("The most frequent character is '%c', it appeared %d times.\n", mostFrequentChar, maxFreq);
    } else {
        printf("Error\n");
    }

    return 0;
}