#include "builder.h"

void builder::run() {

        C_MatrixXd *result = NULL;

        isinited = true;

        std::cout << " in builder run " << std::endl;

        list<step<C_MatrixXd> *>::iterator i;
        for(i=this->steps.begin(); i != this->steps.end(); ++i) {

              step<C_MatrixXd> *s = *i;

              std::cout << " step name = ";
              std::cout <<  s->getName() << std::endl;

              if(result != NULL)
                  s->addToInput(result);

             
              matmul *new_d = dynamic_cast<matmul*>(s);

              redux *new_r = dynamic_cast<redux*>(s);

              std::cout << " mmul "  << std::endl;
              std::cout << new_d << std::endl;
              std::cout << " redux  "  << std::endl;
              std::cout << new_r << std::endl;

              
           //   if(new_d != NULL)
           //       new_d->apply();
           //   else if(new_r != NULL)
           //       new_r->apply();
              

               s->apply();

              std::cout << " run apply  "  << std::endl;

              if(s->shouldPrintSet())
                 MatrixXd_print(s->getResult());

              std::cout << " aft print  "  << std::endl;

              result = s->getResult();
              
              std::cout << " run result  "  << result << std::endl;

        }
        this->last_result = result;

              std::cout << " run done  "  << std::endl;
}

