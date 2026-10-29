#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#define ARCHIVE_PATH "/home/player/flag7/bran.tar.gz"
#define CLEANUP_PATH "/tmp/lain"
#define FLAG_PATH    "/opt/potty"

/* Returns 1 if path exists (any type), 0 otherwise. */
static int path_exists(const char *path) {
    struct stat st;
    return stat(path, &st) == 0;
}

static void print_flag(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) {
        perror("myname");
        exit(1);
    }
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        fputs(line, stdout);
    }
    fclose(fp);
}

int main(void) {
    if (path_exists(ARCHIVE_PATH)) {
        printf("Sealed in gzip's grip, a secret waits - only tar's gentle hand can set it free. Don't forget to delete the .tar.gzip after that.\n");
        return 0;
    }

    if (path_exists(CLEANUP_PATH)) {
        printf("Not yet - some debris still lingers at %s. Clear it away.\n", CLEANUP_PATH);
        return 1;
    }

    print_flag(FLAG_PATH);
    return 0;
}