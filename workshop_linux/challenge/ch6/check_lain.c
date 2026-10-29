#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define TARGET_FILE  "/tmp/lain"
#define TARGET_TEXT  "Wubba lubba dub dub"
#define FLAG_PATH    "/opt/naughty"

/* Returns 1 if path exists and is a regular file, 0 otherwise. */
static int file_exists(const char *path) {
    struct stat st;
    if (stat(path, &st) != 0) return 0;
    return S_ISREG(st.st_mode);
}

/* Reads the file (capped at 4KB) and checks whether target appears
   anywhere in it - doesn't matter which line it's on. */
static int text_found_in_file(const char *path, const char *target) {
    FILE *fp = fopen(path, "r");
    if (!fp) return 0;

    char buf[4096];
    size_t total = 0, n;

    while (total < sizeof(buf) - 1 &&
           (n = fread(buf + total, 1, sizeof(buf) - 1 - total, fp)) > 0) {
        total += n;
    }
    buf[total] = '\0';
    fclose(fp);

    return strstr(buf, target) != NULL;
}

static void print_flag(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) {
        perror("Could not read flag");
        exit(1);
    }
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        fputs(line, stdout);
    }
    fclose(fp);
}

int main(void) {
    if (!file_exists(TARGET_FILE)) {
        printf("Not yet - create %s.\n", TARGET_FILE);
        return 1;
    }

    if (!text_found_in_file(TARGET_FILE, TARGET_TEXT)) {
        printf("Not yet - write \"%s\" into %s.\n", TARGET_TEXT, TARGET_FILE);
        return 1;
    }

    print_flag(FLAG_PATH);
    return 0;
}