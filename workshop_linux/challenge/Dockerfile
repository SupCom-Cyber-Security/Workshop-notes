FROM ubuntu:22.04

# ---------------------------------------------------------------------------
# Packages, users, passwords
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-server \
        sudo \
        socat \
        vim nano less \
        grep sed gawk findutils coreutils \
        tar gzip zip unzip file \
        gcc \
        python3 \
        openssl \
        procps \
        acl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

RUN groupadd players \
    && useradd -m -s /bin/bash -G players player \
    && useradd -m -s /bin/bash -G players blossom \
    && useradd -m -s /bin/bash almost_root \
    && usermod -aG shadow almost_root

# Change these before a real event, or randomize per-instance.
RUN echo "player:player123" | chpasswd \
    && echo "blossom:sunshine99" | chpasswd \
    && echo "almost_root:peekaboo99" | chpasswd

# md5crypt ($1$) instead of SHA-512 - much faster to crack on modest
# hardware (mode 500 in hashcat, --format=md5crypt in John).
RUN usermod -p "$(openssl passwd -1 'abuhamza1')" root

# ---------------------------------------------------------------------------
# Flag 1 - ls, cat
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag1 && \
    echo "SC2{welcome_to_the_shell}" > /home/player/flag1/flag1.txt

# ---------------------------------------------------------------------------
# Flag 2 - hidden dotfile, ls -la
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag2 && \
    echo "SC2{hidden_files_are_still_files}" > /home/player/flag2/.flag2.txt

# ---------------------------------------------------------------------------
# Flag 3 - grep through a large file
# ---------------------------------------------------------------------------
RUN mkdir /home/player/flag3
COPY ch3/challenge.txt /home/player/flag3/flag3.txt

# ---------------------------------------------------------------------------
# Flag 4 - unzip an archive
# Directory must be player-owned so unzip can actually extract into it -
# it was root-owned before, which is why extraction failed with
# "Permission denied". File also renamed to end in .zip, not .txt.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag4 && \
    chown player:players /home/player/flag4
COPY ch4/archive.zip /home/player/flag4/archive.zip
RUN chown player:players /home/player/flag4/archive.zip

# ---------------------------------------------------------------------------
# Flag 5 - just run a binary
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag5/
COPY ch5/execute_me /home/player/flag5/execute_me
COPY ch5/flag5.txt /opt/pointy
RUN chown player:player /home/player/flag5/

RUN chmod 4711 /home/player/flag5/execute_me && \
    chmod 600 /opt/pointy

# ---------------------------------------------------------------------------
# Flag 6 - mkdir + file writing
# Player creates /home/player/flag6/lain containing "Wubba lubba dub dub".
# Directory is chowned to player so they can actually create that file -
# same missing-write-permission bug as flag4 had.
# check_lain (setuid root) verifies this and reveals /opt/naughty, which
# the player otherwise can't read directly.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag6 && \
    chown player:players /home/player/flag6

RUN echo "SC2{h3ll0_w0rld_d3t3ct3d}" > /opt/naughty && \
    chown root:root /opt/naughty && \
    chmod 600 /opt/naughty

COPY ch6/check_lain /home/player/flag6/
RUN chown root:root /home/player/flag6/check_lain && \
    chmod 4711 /home/player/flag6/check_lain

# ---------------------------------------------------------------------------
# Flag 7 - tar, rm
# myname (setuid root) walks the player through extracting bran.tar.gz and
# removing leftover /tmp/lain before revealing the flag from /opt/potty.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag7 && \
    chown player:players /home/player/flag7 && \
    chmod 755 /home/player/flag7

RUN echo "SC2{cl34n_up_4ft3r_y0urs3lf}" > /opt/potty && \
    chown root:root /opt/potty && \
    chmod 600 /opt/potty

COPY ch7/bran.tar.gz /home/player/flag7/bran.tar.gz
COPY ch7/myname /home/player/flag7/myname
RUN chown root:root /home/player/flag7/myname && \
    chmod 4711 /home/player/flag7/myname

# ---------------------------------------------------------------------------
# Bonus flag - 10 dirs full of decoys, a disguised "mirror" file, a setuid
# checker binary, and two fake flags to punish naive `grep -r FLAG`.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flagBonus/dir1 \
             /home/player/flagBonus/dir2 \
             /home/player/flagBonus/dir3 \
             /home/player/flagBonus/dir4 \
             /home/player/flagBonus/dir5 \
             /home/player/flagBonus/dir6 \
             /home/player/flagBonus/dir7 \
             /home/player/flagBonus/dir8 \
             /home/player/flagBonus/dir9 \
             /home/player/flagBonus/dir10 && \
    chown -R player:player /home/player/flagBonus

# Decoy clutter - nothing here matters, it's just noise to search through.
RUN echo "TODO: reorganize this later" > /home/player/flagBonus/dir1/notes.txt && \
    echo "id,value" > /home/player/flagBonus/dir1/data.csv && \
    echo "192.168.1.1 localhost" > /home/player/flagBonus/dir2/hosts.bak && \
    dd if=/dev/urandom of=/home/player/flagBonus/dir2/blob.dat bs=1K count=4 2>/dev/null && \
    printf '#!/bin/bash\necho "nothing here"\n' > /home/player/flagBonus/dir3/run.sh && \
    chmod +x /home/player/flagBonus/dir3/run.sh && \
    echo "temporary file, safe to delete" > /home/player/flagBonus/dir4/.hidden_note && \
    echo "config_version=1.2" > /home/player/flagBonus/dir4/settings.conf && \
    printf 'just some log lines\n[INFO] startup ok\n[WARN] deprecated flag used\n' > /home/player/flagBonus/dir5/app.log && \
    echo "lorem ipsum dolor sit amet" > /home/player/flagBonus/dir7/draft.md && \
    echo "empty placeholder" > /home/player/flagBonus/dir8/placeholder && \
    echo "cache entry 0001" > /home/player/flagBonus/dir9/cache.tmp

# Two fake flags, same format as the real one, planted in plausible spots.
RUN echo "SC2{not_the_flag_you_are_looking_for}" > /home/player/flagBonus/dir3/flag.txt && \
    echo "SC2{not_the_flag_you_are_looking_for}" > /home/player/flagBonus/dir4/flag.txt

# mirror = gzip data with no extension. bin = setuid checker. Both prepared
# locally and copied in, so nothing about their contents leaks into layer
# history.
COPY ch8/mirror /home/player/flagBonus/dir10/mirror
COPY ch8/bin /home/player/flagBonus/dir6/bin
RUN chown root:root /home/player/flagBonus/dir6/bin && \
    chmod 4711 /home/player/flagBonus/dir6/bin

# Real flag - root-owned, outside the player's reachable tree. Only the
# checker binary (running as root via setuid) can read it.
RUN echo "SC2{Well_It_took_You_Long_Enough_To_Find_Me}" > /opt/knotty && \
    chown root:root /opt/knotty && \
    chmod 600 /opt/knotty

# ---------------------------------------------------------------------------
# Flag 8 - find the "blo*" user in /etc/passwd, su to them, read their secret
# Tip about `exit` added since going blossom -> player was tripping people
# up (su back to player needs player's password; exit just pops the shell).
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag8 && \
    printf 'psst... someone left this lying around:\nFind the user whose name starts with blo, his password is: sunshine99\n\ntip: use "exit" to get back to your own shell instead of su-ing again.\n' > /home/player/flag8/creds.txt && \
    echo "SC2{trust_but_verify}" > /home/blossom/secret.txt && \
    chown blossom:blossom /home/blossom/secret.txt && \
    chmod 600 /home/blossom/secret.txt

# ---------------------------------------------------------------------------
# Flag 9 - chmod/chown practice, then fix gimmick/'s missing execute bit
# to cd in and read the flag inside. Parent dir chowned to player so they
# can actually create the "bloody" practice file inside it.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag9/gimmick && \
    chown player:players /home/player/flag9 && \
    echo "SC2{execute_bit_or_no_entry}" > /home/player/flag9/gimmick/flag9.txt && \
    chown blossom:players /home/player/flag9/gimmick/flag9.txt && \
    chmod 640 /home/player/flag9/gimmick/flag9.txt && \
    chown player:players /home/player/flag9/gimmick && \
    chmod 644 /home/player/flag9/gimmick

# ---------------------------------------------------------------------------
# Flag 10 - "monster" (setuid root). A README nudges players toward it.
# Find MONSTER_SECRET with `env`, feed it to the binary when prompted, and
# it reveals /opt/saucy - unreadable to the player directly.
# ---------------------------------------------------------------------------
RUN mkdir -p /home/player/flag10 && \
    cat > /home/player/flag10/README.txt <<'EOF'
There's a binary called "monster" hiding somewhere on this system.
Find it, and see what it wants.
EOF

RUN mkdir -p /opt && \
    echo "SC2{feed_the_monster_what_it_wants}" > /opt/saucy && \
    chown root:root /opt/saucy && \
    chmod 600 /opt/saucy

ENV MONSTER_SECRET="Johan_Liebert"

COPY ch11/monster /usr/local/bin/monster
RUN chown root:root /usr/local/bin/monster && \
    chmod 4755 /usr/local/bin/monster

# ---------------------------------------------------------------------------
# Flag 11 - crack root's hash from /etc/shadow (on their own machine),
# su root, read the final flag. almost_root's credentials are handed over
# directly here - being in the shadow group isn't itself the puzzle, the
# hash-cracking is.
# ---------------------------------------------------------------------------
RUN mkdir -p /root && \
    echo "SC2{r00t_w4s_n3v3r_th4t_f4r}" > /root/flag11.txt && \
    chmod 600 /root/flag11.txt && \
    mkdir -p /home/player/flag11 && \
    cat > /home/player/flag11/README.txt <<'EOF'
    Have you heard of the hidden art known as Privilege Escalation?

    Your next target awaits:
    User: almost_root
    Password: peekaboo99
EOF
# ---------------------------------------------------------------------------
# Drop to the player account for the shell everyone actually connects to.
# ---------------------------------------------------------------------------

RUN echo "export TERM=xterm" >> /etc/bash.bashrc
USER player
WORKDIR /home/player

EXPOSE 4444
CMD ["socat", "TCP-LISTEN:4444,reuseaddr,fork", "EXEC:/bin/bash,pty,stderr,setsid,sigint,sane"]
#socat file:`tty`,raw,echo=0 tcp:<host>:<port>