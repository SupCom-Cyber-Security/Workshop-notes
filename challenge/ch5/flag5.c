#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // Elevate effective user ID to root
    if (setuid(0) != 0) {
        perror("Failed to set UID to root");
        return 1;
    }

    // Open the target file
    FILE *file = fopen("/opt/pointy", "r");
    if (file == NULL) {
        perror("Error opening /opt/pointy");
        return 1;
    }

    // Read and print the contents to standard output
    char buffer[1024];
    size_t bytes_read;
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        fwrite(buffer, 1, bytes_read, stdout);
    }

    fclose(file);
    return 0;
}