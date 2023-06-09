#ifdef LOG1
#include "log1.h"
#else
#include "log.h"
#endif

int main(int argc, char* argv[])
{
    try
    {
        FILELog::ReportingLevel() = FILELog::FromString(argv[1] ? argv[1] : "DEBUG1");
	    const int count = 3;
        FILE_LOG(logDEBUG) << "A loop with " << count << " iterations";
        for (int i = 0; i != count; ++i)
        {
	        FILE_LOG(logDEBUG1) << "the counter i = " << i;
        }
        return 0;
    }
    catch(const std::exception& e)
    {
        FILE_LOG(logERROR) << e.what();
    }
    return -1;
}
