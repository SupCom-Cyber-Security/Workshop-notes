/*
 * bin.c - bonus flag checker with step-by-step guidance
 *
 * Solve path enforced by this checker, in order:
 *   1. Create file1 in dir1 containing "I love my life"
 *   2. Move file1 into dir6
 *   3. Create file2 in dir6 containing file1's new absolute path
 *   4. Identify mirror's real type (dir10) via `file` and pass it as argv[1]
 *
 * Compile:  gcc -O2 -o bin bin.c
 * Deploy:   chown root:root bin && chmod 711 bin
 *           chown root:root /opt/knotty && chmod 600 /opt/knotty
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <limits.h>
#include <unistd.h>

#define BASE          "/home/player/flagBonus"
#define FILE1_ORIGIN  BASE "/dir1/file1"
#define FILE1         BASE "/dir6/file1"
#define FILE2         BASE "/dir6/file2"
#define MIRROR        BASE "/dir10/mirror"
#define FLAG_PATH     "/opt/knotty"
#define EXPECTED_TEXT "I love my life"

static int file_exists(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISREG(st.st_mode);
}

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

static int read_first_line(const char *path, char *out, size_t out_size) {
    FILE *fp = fopen(path, "r");
    if (!fp) return 0;
    if (!fgets(out, out_size, fp)) { fclose(fp); return 0; }
    out[strcspn(out, "\n")] = '\0';
    fclose(fp);
    return 1;
}

/* execve-based, no shell, no PATH lookup - avoids the popen/PATH hijack
   risk of shelling out to `file` via /bin/sh -c. */
static int get_mirror_type(char *out, size_t out_size) {
    int pipefd[2];
    if (pipe(pipefd) != 0) return 0;

    pid_t pid = fork();
    if (pid < 0) return 0;

    if (pid == 0) {
        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[0]);
        close(pipefd[1]);
        char *argv[] = { "file", "-b", MIRROR, NULL };
        char *envp[] = { NULL };
        execve("/usr/bin/file", argv, envp);
        _exit(127);
    }

    close(pipefd[1]);
    ssize_t r = read(pipefd[0], out, out_size - 1);
    close(pipefd[0]);
    waitpid(pid, NULL, 0);

    if (r <= 0) return 0;
    out[r] = '\0';
    out[strcspn(out, "\n")] = '\0';
    return 1;
}

static void print_flag(void) {
    FILE *fp = fopen(FLAG_PATH, "r");
    if (!fp) { perror("bin"); exit(1); }
    char line[256];
    while (fgets(line, sizeof(line), fp)) fputs(line, stdout);
    fclose(fp);
}

int main(int argc, char *argv[]) {

    /* --- Step 1: file1 must first exist in dir1 with correct content --- */
    if (!file_exists(FILE1)) {
        if (!file_exists(FILE1_ORIGIN)) {
            printf(
                "[Step 1/4] file1 not found.\n"
                "  -> Create a file named 'file1' in dir1 containing:\n"
                "I'm not going there to die. I'm going to find out if I'm really alive.\n"
            );
            return 1;
        }
        if (!text_found_in_file(FILE1_ORIGIN, EXPECTED_TEXT)) {
            printf(
                "[Step 1/4] file1 exists in dir1 but doesn't contain the expected sentence.\n"
                "  -> It must contain exactly: \"%s\"\n",
                EXPECTED_TEXT
            );
            return 1;
        }

        /* file1 exists in dir1 with correct content -> tell them to move it */
        printf(
            "[Step 2/4] file1 looks correct in dir1.\n"
            "  -> Now move it into dir6:\n"
        );
        return 1;
    }
    if (!text_found_in_file(FILE1, EXPECTED_TEXT)) {
        printf(
            "[Step 2/4] file1 is in dir6 but doesn't contain the expected sentence.\n"
            "  -> It must contain exactly: \"%s\"\n",
            EXPECTED_TEXT
        );
        return 1;
    }

    /* --- Step 3: file2 must hold file1's new absolute path --- */
    char expected_path[PATH_MAX];
    if (!realpath(FILE1, expected_path)) { perror("bin"); return 1; }

    char file2_content[PATH_MAX];
    if (!file_exists(FILE2) ||
        !read_first_line(FILE2, file2_content, sizeof(file2_content)) ||
        strcmp(file2_content, expected_path) != 0) {
        printf(
            "[Step 3/4] file2 is missing or doesn't contain file1's correct path.\n"
            "  -> Create 'file2' in dir6 containing file1's ABSOLUTE path (its NEW\n"
            "     location, after the move):\n"
        );
        return 1;
    }

    /* --- Step 4: identify mirror's real type and pass it as argv[1] --- */
    if (argc < 2) {
        printf(
            "[Step 4/4] file1 and file2 look good.\n"
            "  -> Now find the disguised file 'mirror' somewhere in dir1-dir10\n"
            "     and identify its real type:\n"
            "  -> Then run this program again, passing that type string as an\n"
            "     argument (quoted, since it contains spaces):\n"
            "       ./bin \"<file type string>\"\n"
        );
        return 1;
    }

    char mirror_type[512];
    if (!get_mirror_type(mirror_type, sizeof(mirror_type))) {
        printf("[Step 4/4] internal error identifying mirror's type. Is 'file' installed?\n");
        return 1;
    }

    if (strcmp(argv[1], mirror_type) != 0) {
        printf(
            "[Step 4/4] That's not the right type for mirror.\n"
            "  -> and pass the exact output (quoted) as the argument.\n"
        );
        return 1;
    }

    print_flag();
    return 0;
}