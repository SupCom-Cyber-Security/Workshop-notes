FROM php:8.2-apache

# 1. Installation des extensions
RUN docker-php-ext-install mysqli \
    && a2enmod rewrite

# 2. Masquage des en-têtes de version (Security Hardening)
RUN echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
    && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && echo "expose_php = Off" > /usr/local/etc/php/conf.d/security.ini

# 3. Copie du code source dans le dossier web
COPY . /var/www/html/

# 4. Protection des fichiers source en lecture seule pour www-data
RUN chown -R root:root /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80