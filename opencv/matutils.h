#include <iostream>
#include <cstdlib>
#include <Eigen/Core>

using namespace Eigen;

class marker {

   public:
    char *getName() { return ""; }

};


class matutils {

    public:

        C_MatrixXd *call_MatrixXd_new_from_array(double *coeff_1_d, int cols, int rows) {

            MatrixXd *xm = new MatrixXd(cols, rows);

            double *d = &(*xm)(0);

            std::memcpy(d, coeff_1_d, rows * cols * sizeof(*d));

            typedef Map<MatrixXd> MapType;

            MapType m2map(d, rows, cols);               

            
            return eigen_to_c(*xm);
        }

        static MatrixXd &call_MatrixXd_new_random(int cols, int rows) {
            MatrixXd m = MatrixXd::Random(cols, rows); 
            return m;
        }

        static Map<MatrixXd> &call_MatrixXd_new_random01(int cols, int rows) {

            double rands[100];
            for(int i=0;i<100;i++)
                rands[i] = rand()%1;

            Map<MatrixXd> mmap(rands, cols, rows);
            return mmap;
 
        }

        static Map<MatrixXd> &call_MatrixXd_new_random100(int cols, int rows) {

            double rands[100];
            for(int i=0;i<100;i++)
                rands[i] = rand()%100;

            Map<MatrixXd> mmap(rands, cols, rows);
            return mmap;
 
        }

        static Map<MatrixXd> &call_MatrixXd_new_random0n(int cols, int rows, double n) {
  
            double rands[100];
            for(int i=0;i<100;i++)
                rands[i] = rand()%1 * n;

            Map<MatrixXd> mmap(rands, cols, rows);
            return mmap;
        }

};
