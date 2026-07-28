#ifndef MSCONNECTOR_HEADER_VALIDATION_INTERNAL_H
#define MSCONNECTOR_HEADER_VALIDATION_INTERNAL_H

#include "msconnector/headers.h"

#include <stddef.h>

static inline int
msconnector_header_is_valid(const msconnector_header *header)
{
    if (header == 0 || header->name == 0 || header->name_size == 0U) {
        return 0;
    }

    for (size_t index = 0; index < header->name_size; ++index) {
        unsigned char ch = (unsigned char)header->name[index];

        if (ch <= 32U || ch == 127U || ch == ':') {
            return 0;
        }
    }

    return header->value != 0 || header->value_size == 0U;
}

#endif
