#include "ngx_http_modsecurity_common.h"
#include "nginx-host-observation.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
uint64_t msconnector_lifecycle_host_begin(void) { errno=EIO; return 17; }
int msconnector_lifecycle_host_end(uint64_t c,const void *h,const msconnector_transaction_contract *t,const Transaction *n,int r) { (void)c;(void)h;(void)t;(void)n;(void)r;errno=EIO;return 0; }
uint64_t msconnector_lifecycle_host_scope_call(const void *h) { (void)h;errno=EIO;return 0; }
int msconnector_lifecycle_host_retire(const void *h) { (void)h;errno=EIO;return 0; }
int main(int argc,char **argv) {
 ngx_http_modsecurity_ctx_t ctx; ngx_http_request_t request; ngx_connection_t connection;
 char fdstr[32]; int fd; char row[2048]; ssize_t size;
 assert(argc==2); memset(&ctx,0,sizeof(ctx));memset(&request,0,sizeof(request));memset(&connection,0,sizeof(connection));
 ctx.r=&request;request.connection=&connection;request.header_sent=1;connection.sent=129;
 errno=ERANGE;assert(ngxi12_host_begin()==17);assert(errno==ERANGE);
 ngxi12_host_end(17,&ctx,&ctx.contract,NULL,0);assert(errno==ERANGE);
 ngxi12_host_retire(&ctx);assert(errno==ERANGE);
 assert(unsetenv("MSCONNECTOR_NGX_HOST_FD")==0);
 ngxi12_host_note(&ctx,"request_eos",1,0,0);assert(errno==ERANGE);
 fd=open(argv[1],O_RDWR|O_CREAT|O_EXCL|O_APPEND,0600);assert(fd>=3);
 (void)snprintf(fdstr,sizeof(fdstr),"%d",fd);assert(setenv("MSCONNECTOR_NGX_HOST_FD",fdstr,1)==0);
 errno=ERANGE;ngxi12_host_note(&ctx,"request_eos",1,0,0);assert(errno==ERANGE);
 assert(lseek(fd,0,SEEK_SET)==0);size=read(fd,row,sizeof(row)-1);assert(size>0);row[size]='\0';
 assert(strstr(row,"\"allocation_scope_call\":0")!=NULL); /* unmapped never becomes joined */
 assert(strstr(row,"\"last_buf\":1")!=NULL);assert(strstr(row,"\"remaining\":0")!=NULL);
 assert(strstr(row,"\"header_sent\":1")!=NULL);assert(strstr(row,"\"connection_sent\":129")!=NULL);
 assert(setenv("MSCONNECTOR_NGX_HOST_FD","not-a-descriptor",1)==0);
 errno=ERANGE;ngxi12_host_note(&ctx,"response_eos",0,1,-1);assert(errno==ERANGE);
 assert(lseek(fd,0,SEEK_END)==size);assert(close(fd)==0);return 0;
}
