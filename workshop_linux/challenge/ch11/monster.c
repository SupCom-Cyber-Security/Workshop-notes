/*
 * monster.c
 * ---------------------------------------------------------------------
 * SUID-root binary for flag 10.
 *
 * Behavior:
 *   - Reads the expected secret from the MONSTER_SECRET environment
 *     variable (set globally for login shells - the player finds it
 *     with `env`).
 *   - Prompts the player to type the secret.
 *   - If it matches, opens /opt/saucy (root:root, 600 - unreadable by
 *     the player directly) and prints its contents. This only works
 *     because the binary runs with root's effective UID via the SUID bit.
 *   - If it doesn't match, refuses.
 *
 * Compile on your local machine (NOT inside the Dockerfile, per your
 * request), then just COPY the resulting binary into the image:
 *
 *     gcc -Wall -O2 -o monster monster.c
 *
 * Keep the source next to your Dockerfile if you want to recompile later,
 * but only the compiled `monster` binary needs to be in the build context.
 * ---------------------------------------------------------------------
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_LEN 128
#define FLAG_PATH "/opt/saucy"

int main(void) {
    const char *expected = getenv("MONSTER_SECRET");
    char input[MAX_LEN];

    if (expected == NULL) {
        fprintf(stderr, "The monster is asleep and cannot be reached right now.\n");
        return 1;
    }

    printf("You have awoken the monster. It demands a secret.\n");
    printf("Enter the secret: ");
    fflush(stdout);

    if (fgets(input, sizeof(input), stdin) == NULL) {
        fprintf(stderr, "No input received.\n");
        return 1;
    }
    input[strcspn(input, "\n")] = '\0'; /* strip trailing newline */

    if (strcmp(input, expected) != 0) {
        printf("Wrong secret. The monster is not pleased.\n");
        return 1;
    }

    FILE *f = fopen(FLAG_PATH, "r");
    if (f == NULL) {
        perror("Unable to open flag file");
        return 1;
    }

    char line[256];
    while (fgets(line, sizeof(line), f) != NULL) {
        printf("%s", line);
    }
    fclose(f);

    return 0;
}