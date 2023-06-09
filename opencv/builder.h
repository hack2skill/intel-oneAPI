#include <Eigen/Core>
#include "workflow.h"

using namespace Eigen;
using namespace dsl;


class builder {

   private:

     step<MatrixXd>  algostep;

     list<step<C_MatrixXd> *>  steps;

     bool isinited;

     C_MatrixXd *last_result;

   public:

     builder() {
         isinited = false;
     }

     step<MatrixXd> getStep() {
         return this->algostep;
     }

     MatrixXd *getResult() {
       if(!isinited)
          std::cout << " workflow not run. first run workflow to see result " << std::endl;

          return & c_to_eigen(this->last_result);
     }

     matmul &newmatmul(char *name, bool repeat, int stride, int tile=0) { return *(new matmul(name, repeat, stride, tile)); }

     redux &newredux(char *name)  { return *(new redux(name)); }

     convolve &newconvolve(char *name) { return *(new convolve(name)); }

     void addStep(step<C_MatrixXd> *s) { steps.push_back(s); }

     list<step<C_MatrixXd> *>getSteps() {
         return this->steps;
     }

     void run();

};







