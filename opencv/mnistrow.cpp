#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>


#include "builder.h"
#include "matutils.h"


bool is_header;
int rowNum = 0;

int toint(std::string s);

class CSVRow
{
    public:

        CSVRow() {

        }

        std::string const& operator[](std::size_t index) const
        {
            return m_data[index];
        }
        std::size_t size() const
        {
            return m_data.size();
        }

        void readNextRow(std::istream& str)
        {

            std::string         line;
            std::getline(str, line);

            std::stringstream   lineStream(line);
            std::string         cell;

            m_data.clear();
            bool isFirst = true;
            int k=0;

            while(std::getline(lineStream, cell, ','))
            {

                if(rowNum == 0) {
                    is_header = true;
                    return;
                }

                if(isFirst) {
                  label = cell; 
                  isFirst = false;
                  continue;
                }
                m_data.push_back(cell);

            }


        }

        std::vector<std::string> get_data() {
            return m_data;
        }

        std::string get_label() {
            return label;
        }

        void setnumitems(int n) {
            this->numitems = n;
        }

        
    private:
        std::vector<std::string>    m_data;
        std::string label;
        int numitems;


};

std::istream& operator>>(std::istream& str, CSVRow& data)
{
    data.readNextRow(str);
    rowNum++;
    return str;
}   

int main()
{
    std::ifstream       file("file-mnist-trainset.csv");


    int NUM_IMAGES = 4244;
    int NUM_COLS = 28, NUM_ROWS=28;

    std::vector<unsigned char **> m_images;

    CSVRow              row;
    row.setnumitems(784);

    std::vector<CSVRow> rows;

    while(file >> row)
    {

        if(is_header) {
            is_header = false;
            continue;
        }

        unsigned char **mnist_Images = new unsigned char *[NUM_ROWS];

        for(int d=0;d<NUM_ROWS;d++)
           mnist_Images[d] = new unsigned char[NUM_COLS];


      //  std::cout << "rowlabel" << row.get_label() << std::endl;

        std::vector<std::string> rowdata = row.get_data();
       
     //   std::cout << "rowdata sz" << rowdata.size() << std::endl;

        int idx = 0; 
        std::vector<std::string>::iterator iter; 
        for(iter=rowdata.begin(); iter != rowdata.end(); ++iter) {

            std::string celldata = *iter;
            
            int p = idx % NUM_COLS; 
            int q = (int) idx / NUM_ROWS;

            mnist_Images[p][q] = toint(celldata);

            idx++;
        }
        
          
            /*
            for(int p=0;p<NUM_COLS;p++) {
                for(int q=0;q<NUM_ROWS;q++) {
                    std::cout << (int) mnist_Images[p][q]; 
                }
                    std::cout << std::endl;
            }
            */
            
        m_images.push_back(mnist_Images);

        rows.push_back(row);
    }

        std::vector<unsigned int **> vimgs;
        unsigned int **m_img;

        std::vector<std::string> imgrows;

        int x = 0;
        std::vector<unsigned char **>::iterator iter; 
        for(iter=m_images.begin(); iter != m_images.end(); ++iter) {
            unsigned char **mnistImage = *iter; 

            m_img = new unsigned int *[28];
            for(int i=0;i<28;i++) 
                m_img[i] = new unsigned int[28];

            for(int p=0;p<NUM_COLS;p++) {
                for(int q=0;q<NUM_ROWS;q++) {
                //    std::cout << (int) mnistImage[p][q];
                    m_img[p][q] = (int) mnistImage[p][q];
                }
               //     std::cout << std::endl;
            }

          //  std::cout << "label = " << rows[x++].get_label() << std::endl;

            vimgs.push_back(m_img);

            imgrows.push_back(rows[x].get_label());

            x++;
            if(x>15)
              break;

        }
        

           std::cout << "echo vimgs size = " << vimgs.size() << std::endl;

           x=0;
           std::vector<unsigned int **>::iterator it; 
           for (it = vimgs.begin(); it!=vimgs.end(); ++it) {
              unsigned int **v_img = *it;
              std::cout << "echo vimg  = " << v_img << std::endl;
              for(int p=0;p<NUM_COLS;p++) {
                 for(int q=0;q<NUM_ROWS;q++) {
                    std::cout << (int) v_img[p][q];
                }
                    std::cout << std::endl;
              }

                    std::cout << "label = " << imgrows[x++] << std::endl;
           }


    

       matutils *mutils = new matutils();

       builder *b = new builder();

       double dummy[784];
       const C_MatrixXd *resultMatMult = 
                  MatrixXd_new_from_array(dummy, NUM_COLS, NUM_ROWS);

       const C_MatrixXd *resultReduc = 
                  MatrixXd_new_from_array(dummy, NUM_COLS, NUM_ROWS);


        int mmrows = MatrixXd_get_size_rows(resultMatMult);
        int mmcols = MatrixXd_get_size_cols(resultMatMult);

        std::cout << "mmrows = " << mmrows << std::endl;
        std::cout << "mmcols = " << mmcols <<  std::endl;

        std::cout << "init = " << std::endl;

       double coeff[4][4];
       double *coeff_1_d= (double *) coeff;

       coeff[0][0] = 1;
       coeff[0][1] = 0;
       coeff[0][2] = 0;
       coeff[0][3] = 0;
       coeff[1][0] = 1;
       coeff[1][1] = 1;
       coeff[1][2] = -1;
       coeff[1][3] = 0;
       coeff[2][0] = 0;
       coeff[2][1] = 1;
       coeff[2][2] = 0;
       coeff[2][3] = 0;
       coeff[3][0] = 1;
       coeff[3][1] = 0;
       coeff[3][2] = -1;
       coeff[3][3] = 1;

       for(int p=0;p<4;p++)
           for(int q=0;q<4;q++)
               coeff_1_d[p * 4 + q] = coeff[p][q];

        std::cout << "init coeff = " << std::endl;

       C_MatrixXd *mcoeff = mutils->call_MatrixXd_new_from_array(coeff_1_d, 4, 4);

       double *signal_1_d = new double[NUM_ROWS * NUM_COLS];

       std::vector<unsigned int **>::iterator itm; 
       for (itm = vimgs.begin(); itm!=vimgs.end(); ++itm) {
          unsigned int **v_img = *itm;

           for(int p=0;p<NUM_ROWS;p++)
               for(int q=0;q<NUM_COLS;q++) {
                   signal_1_d[p * NUM_ROWS + q] = (double) v_img[p][q];

               }

       
           C_MatrixXd *m_signal = mutils->call_MatrixXd_new_from_array(signal_1_d, NUM_ROWS, NUM_COLS);

           matmul m = b->newmatmul("MATMULT", true, 0, 0);

           b->addStep(&m);

           m.setTimer().addToInput(m_signal).setParameter(mcoeff).setResultMatrix(resultMatMult).printResult();

           b->run();
       
           std::cout << " loop end " << std::endl;
           break;
       }

       
    
}

int toint(std::string s)
{
    return std::atoi(s.c_str());
}

