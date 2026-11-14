#include "core.hpp"
#include <cassert>
int main(){sumi::LogFilter f(sumi::Level::Warn);assert(!f.ingest("INFO","boot"));assert(f.ingest("WARN","heat"));assert(f.ingest("ERROR","stop"));assert(!f.ingest("CRITICAL","bad"));assert(!f.ingest("ERROR",""));assert(!f.ingest("ERROR",std::string(161,'x')));assert(f.accepted()==2&&f.rejected()==4);}
