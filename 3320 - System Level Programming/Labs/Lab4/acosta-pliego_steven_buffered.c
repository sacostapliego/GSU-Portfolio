#include <fcntl.h>   // For open()
#include <unistd.h>  // For write() and close()
#include <stdio.h>   // For perror()
#include <time.h>

int main() {
    // Open the file for writing (creates the file if it doesn't exist)
    int fd = open("buffered.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);

    // Check if the file opened successfully
    if (fd == -1) {
        perror("Error opening file");
        return 1;
    }

    const char *message = "Hello There!\n";
    ssize_t bytes_written;
    int i;
    
    //Measure time
    time_t start_time = time(NULL);

    //Write 1000 times
    for (i = 1; i <= 1000; i++) {
        bytes_written = write(fd, message, 13);  // 13 bytes in "Hello There!\n"
        
        //Check if the write was successful
        if (bytes_written == -1) {
            perror("Error writing to file");
            close(fd);  // Close the file descriptor
            return 1;
        }

        //Print the staement from the lab
        printf("%d: Called write(3, str_to_write, 13) which returned that %zd bytes were written\n", i, bytes_written);
    }

    //Measure time after writing
    time_t end_time = time(NULL);

    //Output the elapsed time
    printf("Buffered IO Time elapsed: %ld seconds\n", end_time - start_time);

    //Close the file descriptor
    close(fd);

    return 0;
}