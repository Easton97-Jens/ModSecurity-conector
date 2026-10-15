#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <openssl/sha.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
extern int __real_SSL_write(SSL *,const void *,int);
static uint64_t wall(void) {
    struct timespec now;
    if(clock_gettime(CLOCK_REALTIME,&now)!=0)return 0U;
    return (uint64_t)now.tv_sec*UINT64_C(1000000000)+(uint64_t)now.tv_nsec;
}
int __wrap_SSL_write(SSL *ssl,const void *buffer,int size) {
    const int before_errno=errno;uint64_t before=wall();errno=before_errno;
    int result=__real_SSL_write(ssl,buffer,size);const int saved=errno;uint64_t after=wall();
    char hex[SHA256_DIGEST_LENGTH*2U+1U]={0};char digest_value[67]="null";
    const char *missing="\"SSL_write did not return a positive bounded output byte count\"";
    unsigned char digest[SHA256_DIGEST_LENGTH];
    if(result>0 && result<=size && buffer!=NULL) {
        /* Never consume/change a preexisting native OpenSSL error queue.
         * Only clear helper-owned errors after observing the queue empty. */
        if(ERR_peek_error()!=0UL) missing="\"Native OpenSSL error queue occupied; helper hashing skipped\"";
        else {
            if(SHA256(buffer,(size_t)result,digest)!=NULL) {
                for(size_t i=0;i<SHA256_DIGEST_LENGTH;++i)(void)snprintf(hex+2U*i,3,"%02x",digest[i]);
                (void)snprintf(digest_value,sizeof(digest_value),"\"%s\"",hex);missing="null";
            } else missing="\"Helper SHA256 failed; only helper-owned OpenSSL errors cleared\"";
            ERR_clear_error();
        }
    }
    fprintf(stderr,"HAPROXY_TLS_WRITE {\"function\":\"SSL_write\",\"before_wall_ns\":%llu,\"after_wall_ns\":%llu,\"input_bytes\":%d,\"actual_result\":%d,\"positive_output_sha256\":%s,\"output_digest_missing_reason\":%s,\"opaque_ssl_scope_not_inferred\":true}\n",(unsigned long long)before,(unsigned long long)after,size,result,digest_value,missing);
    errno=saved;return result;
}
