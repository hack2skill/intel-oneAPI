#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>


#include "builder.h"
#include "matutils.h"

#include "CSVRow.h"

#include "log1.h"

using namespace dsl;

extern bool is_header;


istream &operator>>(istream &ifs, CSVRow &row);

extern void maindft();
extern void mainfft2();
//int main(int argc, char **argv)
int main()
{

      //FILELog::ReportingLevel() = FILELog::FromString(argv[1] ? argv[1] : "INFO");
      FILELog::ReportingLevel() = FILELog::FromString("INFO");


        FILE_LOG(logINFO) << "DEEP LEARNING PROGRAM ENVIRO COMMENCING ";
        FILE_LOG(logDEBUG) << "DEBUG MSG";
        FILE_LOG(logERROR) << "ERR MSG";
        FILE_LOG(logWARNING) << "WARN MSG";
        FILE_LOG(logINFO) << "DEEP LEARNING PROGRAM ENVIRO COMMENCING ";


    std::ifstream       file("file-mnist-trainset.csv");


    int NUM_IMAGES = 4244;
    int NUM_COLS = 28, NUM_ROWS=28;

    std::vector<unsigned char **> m_images;

    CSVRow              row;
    row.setnumitems(784);

    std::vector<CSVRow> rows;

    while(file >> row)
    {

        std::vector<std::string> m_data = row.get_data();

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

        }
        
         std::vector<unsigned char **>().swap(m_images);

         std::vector<CSVRow>().swap(rows);

           std::cout << "num labels = " << x << std::endl;
           FILE_LOG(logDEBUG) << " echo vimgs size = "  << vimgs.size();

       //    x=0;
       //    std::vector<unsigned int **>::iterator it; 
       //    for (it = vimgs.begin(); it!=vimgs.end(); ++it) {
       //       unsigned int **v_img = *it;
           //   std::cout << "echo vimg  = " << v_img << std::endl;
          //    FILE_LOG(logDEBUG) << "echo vimg  = " << v_img;

              /*
              for(int p=0;p<NUM_COLS;p++) {
                 for(int q=0;q<NUM_ROWS;q++) {
                  //  std::cout << (int) v_img[p][q];
                    FILE_LOG(logDEBUG) <<  (int) v_img[p][q];
                }
                  //  std::cout << std::endl;
                    FILE_LOG(logDEBUG) <<  std::endl;
              }
              */

                 //   std::cout << "label = " << imgrows[x++] << std::endl;
               //     FILE_LOG(logDEBUG) << "label = " << imgrows[x++];
      //     }


    

       matutils *mutils = new matutils();

       //std::map<std::string, ConfigValue> config_values;
       std::map<std::string, std::string> config_values;

       builder *b = new builder(config_values, "result.txt");

       matmod &m = b->newmatmod("MATMOD", true, 0, 0);

   //    matmul5 &m = b->newmatmul5("MATMUL5", 5, 0, 0);

       b->addStep(&m);

       int dummy[784];
       const C_MatrixXi *resultMatReso = 
                  MatrixXi_new_from_array(dummy, NUM_COLS, NUM_ROWS);

        int mmrows = MatrixXi_get_size_rows(resultMatReso);
        int mmcols = MatrixXi_get_size_cols(resultMatReso);

      //  std::cout << "mmrows = " << mmrows << std::endl;
        FILE_LOG(logDEBUG) << "mmrows = " << mmrows;

        //std::cout << "mmcols = " << mmcols <<  std::endl;
        FILE_LOG(logDEBUG) << "mmcols = " << mmcols;

        //std::cout << "init = " << std::endl;
        FILE_LOG(logDEBUG) << "init = ";

       int *signal_1_d = new int[NUM_ROWS * NUM_COLS];

        //   std::cout << " vimgs sz = " << vimgs.size() << std::endl;

       int loopctr = 0;
       std::vector<unsigned int **>::iterator itm; 
       for (itm = vimgs.begin(); itm!=vimgs.end(); ++itm) {
          unsigned int **v_img = *itm;

           for(int p=0;p<NUM_ROWS;p++)
               for(int q=0;q<NUM_COLS;q++) {
                   signal_1_d[p * NUM_ROWS + q] = (int) v_img[p][q];

               }

       
           C_MatrixXi *m_signal = mutils->call_MatrixXi_new_from_array(signal_1_d, NUM_ROWS, NUM_COLS);

      //     std::cout << " ctr = " << imgrows[loopctr].c_str() << std::endl;

      //     std::cout << " loopctr = " << loopctr << std::endl;

           /*
           values["ID"] = *new ConfigValueIntType(36))); or values["ID"] = ConfigFactory::new_int_type(36);
           values["NAME"] = *new ConfigValueStringType("avin"))); or values["NAME"] = ConfigFactory::new_string_type("avin");

           values.insert(std::make_pair("WEIGHT", *new ConfigValueDoubleType(12.1)));
           values.insert(std::make_pair("BOOL1", *new ConfigValueBoolType(true)));
           values.insert(std::make_pair("BOOL2", *new ConfigValueBoolType(false)));

           values.insert(std::make_pair("ID", *new ConfigValueIntType(36)));
           values.insert(std::make_pair("NAME", *new ConfigValueStringType("avin")));
           values.insert(std::make_pair("WEIGHT", *new ConfigValueDoubleType(12.1)));
           values.insert(std::make_pair("BOOL1", *new ConfigValueBoolType(true)));
           values.insert(std::make_pair("BOOL2", *new ConfigValueBoolType(false)));
           */


           m.setTimer().addToInput(m_signal).setId(loopctr).setLabel(imgrows[loopctr++].c_str()).setResult(resultMatReso).printResult();


      //     b->run();
       
          // std::cout << " loop end " << std::endl;
           FILE_LOG(logDEBUG) << "loop end = ";
       }

   std::cout << " maindft " << std::endl;

  //  maindft();
   mainfft2();


    return 0;
    
}

