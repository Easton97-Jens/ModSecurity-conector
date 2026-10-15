#include <modsecurity/modsecurity.h>
#include <stdio.h>
int main(void) {
    ModSecurity *engine = msc_init();
    if (engine == NULL) return 2;
    const char *identity = msc_who_am_i(engine);
    if (identity == NULL) { msc_cleanup(engine); return 3; }
    (void)puts(identity);
    msc_cleanup(engine);
    return 0;
}
