#pragma once
#include <cstdint>
#include <cstring>
#include <string>
#include <stdexcept>
namespace sumi {
enum class Level {Debug,Info,Warn,Error};
inline bool parseLevel(const std::string& s,Level& out){
 if(s=="DEBUG")out=Level::Debug;else if(s=="INFO")out=Level::Info;
 else if(s=="WARN")out=Level::Warn;else if(s=="ERROR")out=Level::Error;else return false;
 return true;
}
class LogFilter {
 Level minimum_;std::uint32_t accepted_=0,rejected_=0;
public:
 explicit LogFilter(Level minimum):minimum_(minimum){}
 bool ingest(const std::string& level,const std::string& message){
  Level parsed;
  if(message.empty()||message.size()>160||!parseLevel(level,parsed)){++rejected_;return false;}
  if(static_cast<int>(parsed)<static_cast<int>(minimum_)){++rejected_;return false;}
  ++accepted_;return true;
 }
 std::uint32_t accepted()const{return accepted_;}
 std::uint32_t rejected()const{return rejected_;}
};
}
