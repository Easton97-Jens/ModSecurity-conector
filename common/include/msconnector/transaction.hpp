#ifndef MSCONNECTOR_TRANSACTION_HPP
#define MSCONNECTOR_TRANSACTION_HPP
#include "msconnector/transaction.h"
#include "msconnector/transaction_state.h"
namespace msconnector {
using TransactionView = msconnector_transaction_view;
using TransactionState = msconnector_transaction_state;
using Decision = msconnector_decision;
inline const char *phase_name(msconnector_phase phase) noexcept { return msconnector_phase_name(phase); }
}
#endif
