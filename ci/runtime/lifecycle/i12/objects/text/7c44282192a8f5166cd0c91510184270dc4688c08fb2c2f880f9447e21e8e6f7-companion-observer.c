#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <openssl/sha.h>
#include "native-lifecycle-observer.h"
void haproxy_lifecycle_companion_observe(const void *transaction,const char *kind,
        const char *handle,unsigned int actual_operation) {
    const int saved=errno;
    if(handle!=NULL && strlen(handle)==64U) {
        unsigned char digest[SHA256_DIGEST_LENGTH];char hex[65];struct timespec now;
        if(SHA256((const unsigned char *)handle,64U,digest)!=NULL && clock_gettime(CLOCK_REALTIME,&now)==0) {
            for(size_t i=0;i<SHA256_DIGEST_LENGTH;++i)(void)snprintf(hex+2U*i,3,"%02x",digest[i]);
            fprintf(stderr,"HAPROXY_COMPANION_LIFECYCLE {\"kind\":\"%s\",\"scope_call\":%llu,\"capability_sha256\":\"%s\",\"actual_operation\":%u,\"wall_ns\":%llu}\n",kind,(unsigned long long)msconnector_lifecycle_host_scope_call(transaction),hex,actual_operation,(unsigned long long)now.tv_sec*1000000000ULL+(unsigned long long)now.tv_nsec);
        }
    }
    errno=saved;
}
