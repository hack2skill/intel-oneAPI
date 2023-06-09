//#include "readerwriterqueue.h"
//#include "atomicops.h"

#include <iterator>
#include <iostream>
//#include <fstream>
//#include <sstream>
#include <vector>
#include <math.h>
#include <string>
#include <cstdlib>
#include <stdio.h>
#include <stdlib.h>
#include <bits/stdc++.h>
#include <registry.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

//using namespace moodycamel;
using namespace std;
using namespace cv;

struct DFTNode {

    double x;
    double y;

    double x2;
    double y2;

    double *data;

    double ** m_data;
    int num_rows;
    int num_cols;

    int step_id;
    int step_count;

    int num_siblings;

    double * twiddle;

    std::string node_id;

    DFTNode *sub_nodes[4];

    DFTNode *parent;

};

int N;
int bnode = 0;
double _Complex **_twProdFactors;

void buildCoeffs();
void buildSineCoeffs();
void buildCosineCoeffs();
void buildDFTree(struct DFTNode *root, int s, int t);
void buildDFTreeAlt(struct DFTNode *root, int s, int t);
void buildTree(struct DFTNode *root, int s, int t, std::string m);
void buildTree2(struct DFTNode *root, int s, int t, std::string m);
void buildTree4ary(struct DFTNode *root, int s, int t);
void buildTreeTL(struct DFTNode *root, int s, int t);
void buildTreeTR(struct DFTNode *root, int s, int t);
void buildTreeLL(struct DFTNode *root, int s, int t);
void buildTreeLR(struct DFTNode *root, int s, int t);
void printTree(struct DFTNode *root);
void printSubTree(struct DFTNode *root);
bool isPowerOf2(int n);
void fft();
int get_log2(int s);
void do_bfly2(int lz, int batch_size, int num, int start, int nx, int LEVEL_START, int LEVEL_END); 
double _Complex bfly2(int,int,int,int,int, int);
double _Complex bfly3(int,int,int,int,int, int);
void callback_func();
double _Complex get_twiddle(int num);

std::string itoa(int value, int base);

struct DFTNode *xroot;

double **imgPtr;
int m_size;
int m_rows;
int m_cols;

#define POW21512 9

int ** _rowOfIntsX;
int ** _rowOfIntsY;

void (*bflyPtr)(int, int, int, int, int, int, int);
void (*cbfunc)();


int cosineOffset = 10;
double cosineCoeffs [][1] = 
{
    { -9.7 },
    {  -6.20 },
    {  -4.5 },
    { -3.275 },
    { -2.5 },
    { -1.885 },
    { -1.5 },
    { -1.0 },
    { -0.75 },
    { -0.5 },
    { -0.25 },
    { -0 },
    { 0.2 },
    { 0.325 },
    { 0.5 },
    { 0.6 },
    { 0.65 },
    { 0.7 },
    { 0.75 },
    { 0.8 },
    { 0.8 },
    { 0.825 },
    { 0.85 }
};

int sineOffset = 17;
double sineCoeffs [][2] = 

{  
    {  3,  2 },  // 17, 7
    {  1 , 2 },  // 16, 8
    {  3 , 2 },  // 15, 9
    {  2 , 1 },  // 14, 10
    {  2 , 3 },  // 13, 11
    {  1 , 1 },  // 12, 12
    {  3 , 2 },  // 11, 13
    {  1 , 2 },  // 10, 14
    {  2 , 3 },  // 9, 15
    {  2 , 1 },  // 8, 16
    {  1 , 3 },  // 7, 17
    {  3 , 2 },  // 6, 18
    {  1 , 3 },  //5, 19
}; 

/* Function to check if x is power of 2*/
bool isPowerOf2(int n)
{
    if (n == 0)
        return 0;
    while (n != 1)
    {
        if (n%2 != 0)
            return 0;
        n = n/2;
    }
    return 1;
}


/*
double cosines [] = 
{
    -0.999924706,-0.999322425,-0.998118224,-0.99631283,-0.993907329,-0.990903171,-0.987302166,-0.983106481,-0.978318645,-0.972941541,-0.966978408,-0.960432838,-0.953308773,-0.945610504,-0.937342669,-0.928510247,-0.919118557,-0.909173258,-0.898680339,-0.887646121,-0.876077249,-0.863980693,-0.851363737,-0.838233982,-0.824599336,-0.810468011,-0.795848519,-0.780749667,-0.765180548,-0.749150539,-0.732669298,-0.715746749,-0.698393087,-0.680618764,-0.662434486,-0.643851205,-0.624880116,-0.605532644,-0.585820443,-0.565755387,-0.545349562,-0.524615257,-0.503564963,-0.482211357,-0.460567303,-0.438645837,-0.416460162,-0.394023642,-0.371349791,-0.348452266,-0.325344858,-0.302041487,-0.278556188,-0.254903107,-0.231096491,-0.207150679,-0.183080095,-0.158899236,-0.134622669,-0.110265014,-0.085840944,-0.06136517,-0.036852433,-0.0123175,0.012224853,0.036759842,0.06127269,0.085748632,0.110172925,0.134530858,0.158807759,0.182989006,0.207060034,0.231006344,0.254813513,0.2784672,0.30195316,0.325257244,0.348365418,0.371263761,0.393938482,0.416375924,0.438562571,0.460485059,0.482130186,0.503484912,0.524536375,0.545271896,0.565678985,0.585745351,0.605458906,0.624807776,0.643780308,0.662365074,0.680550879,0.698326771,0.71568204,0.732606236,0.749089162,0.765120893,0.78069177,0.795792415,0.810413733,0.824546916,0.838183453,0.851315129,0.863934035,0.876032571,0.887603448,0.898639697,0.909134672,0.91908205,0.92847584,0.937310383,0.94558036,0.953280788,0.960407029,0.96695479,0.972920129,0.978299452,0.983089518,0.987287443,0.990890698,0.993897113,0.996304876,0.998112538,0.99931901,0.999923565
};

double sines [] = 
{
    -0.0122,-0.0368,-0.0613,-0.0857,-0.1102,-0.1345,-0.1588,-0.183,-0.207,-0.231,-0.254,-0.278,-0.301,-0.325,-0.348,-0.371,-0.393,-0.416,-0.438,-0.46,-0.482,-0.503,-0.524,-0.545,-0.565,-0.585,-0.605,-0.624,-0.643,-0.662,-0.68,-0.698,-0.715,-0.732,-0.749,-0.765,-0.78,-0.795,-0.81,-0.824,-0.838,-0.851,-0.863,-0.876,-0.887,-0.898,-0.909,-0.919,-0.928,-0.937,-0.945,-0.953,-0.96,-0.966,-0.972,-0.978,-0.983,-0.987,-0.99,-0.993,-0.996,-0.998,-0.999,-0.999,-0.999,-0.999,-0.998,-0.996,-0.993,-0.99,-0.987,-0.983,-0.978,-0.972,-0.967,-0.96,-0.953,-0.945,-0.937,-0.928,-0.919,-0.909,-0.898,-0.887,-0.876,-0.864,-0.851,-0.838,-0.824,-0.81,-0.795,-0.78,-0.765,-0.749,-0.732,-0.715,-0.698,-0.68,-0.662,-0.643,-0.624,-0.605,-0.585,-0.565,-0.545,-0.524,-0.503,-0.482,-0.46,-0.438,-0.416,-0.394,-0.371,-0.348,-0.325,-0.302,-0.278,-0.255,-0.231,-0.207,-0.183,-0.159,-0.134,-0.11,-0.085,-0.061,-0.036,-0.012
};
*/

int NumEntriesLogOfSizes = 15; 
int LogOfSizes[][1] =
{
    { 2 },
    { 4 },
    { 8 },
    { 16 },
    { 32 },
    { 64 },
    { 128 },
    { 256 },
    { 512 },
    { 1024 },
    { 2048 },
    { 4096 },
    { 8192 },
    { 16384 },
    { 32768 }
};

double sine_coeffs[128][1];
double cosine_coeffs[128][1];

double sineStartVal = 0.012;
double sineStartVal2 = 0.018;
double sineSigma1 = 0.024;
double sineSigma2 = 0.004;

int maindft() {

    /// Read image given by user
    Mat image = imread( "Lenna.png", CV_LOAD_IMAGE_COLOR );


    if(! image.data )                              // Check for invalid input
    {
        cout <<  "Could not open or find the image" << std::endl ;
        return -1;
    }

    Mat new_image = Mat::zeros( image.size(), image.type() );

    /// Initialize values
    std::cout<<" Basic Linear Transforms "<<std::endl;
    std::cout<<"-------------------------"<<std::endl;
    //std::cout<<"* Enter the alpha value [1.0-3.0]: ";std::cin>>alpha;
    //std::cout<<"* Enter the beta value [0-100]: "; std::cin>>beta;


    struct DFTNode *xroot, root;

    //std::stack<int> xy_stack;

    buildCoeffs();

    N = image.rows;

    if(!isPowerOf2(N)) {
        std::cout << "image size not power of 2" << std::endl;
        return;
    }

    root.x = 0;
    root.y = 511;
    root.step_id = 0;
    root.step_count = 1;
    root.num_siblings = 2;
    root.node_id = "0";
    root.parent = NULL; 
    root.sub_nodes[0] = NULL;
    root.sub_nodes[1] = NULL;

    xroot = &root;

    buildDFTree(&root, root.step_count, 0);


    printTree(xroot);
    //   fft();

}


void buildCoeffs() {

    buildCosineCoeffs();
    buildSineCoeffs();
}

void buildSineCoeffs() {

    double sval = sineStartVal;
    for(int i=0;i<32;i++) {
        sine_coeffs[i][0] = sval;
        sval += sineSigma1;
    }


    int k = 0;
    int i =32;
    while(i > 0) {
        int num_times = sineCoeffs[k++][0];
        for(int j=0;i<num_times;j++) {
            sval += sineOffset/1000;
            sine_coeffs[i][0] = sval;
        }

        sineOffset--;
        i+=num_times; 
    }

    for(int i=56;i<73;i++) {
        sine_coeffs[i][0] = 1;
    }


    k = 0;
    i =74;
    double delta = 0.033;
    sval = 1 - delta;
    while(i < 96) {
        int idx = 0;
        int num_times = sineCoeffs[idx++][1];
        for(int p=0;p<num_times;p++) {
            sval += (-1 * (sineOffset-10))/1000;
            sine_coeffs[i+p][0] = sval;
        } 
        i+=num_times; 
    }

    sval += -1 * sineStartVal2;
    for(int i=96;i<128;i++) {
        sine_coeffs[i][0] = sval;
        sval += 0.024;
    }

    for(int k=0;k<128;k++) {
        printf(" Got sin() coeff = %f\n", sine_coeffs[k][0]);
    }


}

void buildCosineCoeffs() {

    for(int k=0;k<10;k++) {
        cosine_coeffs[k][0] = -1.0;
    }

    int incr = cosineOffset;
    for(int i=0;i<23;i+=5) {

        double d = cosineCoeffs[i][0];

        cosine_coeffs[incr][0] = incr * d/100.0;
        incr += 5;

    }

    incr = 5;
    int startpos = rand() % 22;
    int endpos = startpos + 1;

    double s1 = cosineCoeffs[startpos][0];
    double s2 = cosineCoeffs[endpos][0];

    double rate1 = (s2 - s1)/incr;

    startpos = cosineOffset;
    for(int i=1;i<121;i+=5) {
        int spos = startpos;  
        double start_rate = cosineCoeffs[startpos][0];
        spos = startpos + i;  
        cosine_coeffs[spos][0] = startpos * (s1 - (start_rate*1)) / 100.0;
        cosine_coeffs[spos+1][0] = startpos * (s1 - (start_rate*2))/100.0;
        cosine_coeffs[spos+2][0] = startpos * (s1 - (start_rate*3))/100.0;
        cosine_coeffs[spos+3][0] = startpos * (s1 - (start_rate*4))/100.0;
    }

    for(int k=121;k<128;k++) {
        cosine_coeffs[k][0] = 1.0;
    }

    for(int k=0;k<128;k++) {
        printf(" Got cos() coeff = %f\n", cosine_coeffs[k][0]);
    }

}

void fft2(double **imgPtr2, int Size, int rows, int cols) {

    struct DFTNode *xroot, root;

    //std::stack<int> xy_stack;

    N = Size;

    if(!isPowerOf2(N)) {
        std::cout << "image size not power of 2" << std::endl;
        return;
    }

    root.x = 0;
    root.y = 511;
    root.step_id = 0;
    root.step_count = 1;
    root.num_siblings = 2;
    root.node_id = "0";
    root.parent = NULL;
    root.sub_nodes[0] = NULL;
    root.sub_nodes[1] = NULL;

    root.m_data = imgPtr;
    root.num_rows = m_rows;
    root.num_cols = m_cols;

    xroot = &root;

    imgPtr = imgPtr2;
    m_size = Size;
    m_rows = rows;
    m_cols = cols;

    //   buildCoeffs();
    /*
       for(int k=0;k<128;k++) {
       printf(" Got cos() coeff = %f\n", cosines[k]);
       }

       printf(" Got coeff = %f\n\n\n");

       for(int k=0;k<128;k++) {
       printf(" Got sin() coeff = %f\n", sines[k]);
       }
     */

    printf(" calling builddftree  = \n");
    buildDFTree(&root, root.step_count, 0);

    printTree(&root);

    fft();
    printf(" done  = \n");

}

void printTree(struct DFTNode *dfroot) {

    if(dfroot != NULL) {
        //       std::cout <<" on entry   " << dfroot << std::endl;
        //       std::cout <<" on entry :: id = " <<  dfroot->node_id << std::endl;
    }

    if(dfroot == NULL) {
        std::cout <<" is null root = " <<  std::endl;
        return;
    }

    //    std::cout <<" bef subnodes[0] = " << std::endl;
    printTree(dfroot->sub_nodes[0]);   //left
    //     std::cout <<"aft  subnodes[0] = " << std::endl;


    std::cout <<" id, x, y ::  " << std::endl;
    std::cout <<" :: id = " <<  dfroot->node_id << std::endl;

    std::cout << dfroot->node_id << " : " << std::endl;
    std::cout <<  dfroot->x << ", " << dfroot->y << std::endl;

    //  std::cout <<" bef subnodes[1] = " << std::endl;
    printTree(dfroot->sub_nodes[1]);   // right
    //  std::cout <<"aft  subnodes[1] = " << std::endl;
}


void printSubTree(struct DFTNode *dfroot) {

    if(dfroot == NULL) {
        dfroot = dfroot->parent;
        return;
    }


    if(dfroot != NULL) {
        std::cout << dfroot->node_id << " : " << std::endl;
        std::cout <<  dfroot->x << ", " << dfroot->y << std::endl;

        printSubTree(dfroot->sub_nodes[1]);
    }


}

void fft() {


    printf(" enter fft numrows m = \n", m_rows);
    int NUM_COLS = get_log2(m_cols);

    printf(" enter fft numrows  = \n", NUM_COLS);

    double ** rowOfDoubles =  malloc(sizeof(double *) * NUM_COLS);
    int ** rowOfIntsX =  malloc(sizeof(int *) * NUM_COLS);
    int ** rowOfIntsY =  malloc(sizeof(int *) * NUM_COLS);

    for(int k=0;k<NUM_COLS;k++) {
        rowOfDoubles[k] = malloc(sizeof(double) * m_size);
    }

    int *xarr;
    int *yarr;
    int LEVEL_SIZE;
    for(int k=1;k<NUM_COLS;k++) {
        LEVEL_SIZE = pow(2,k);   //pow(2, (k+1)); 

        rowOfIntsX[k] = malloc(sizeof(int) * LEVEL_SIZE);
        rowOfIntsY[k] = malloc(sizeof(int) * LEVEL_SIZE);

        int *xarr = malloc(sizeof(int)*LEVEL_SIZE);
        int *yarr = malloc(sizeof(int)*LEVEL_SIZE);

        int arrsz = m_rows / LEVEL_SIZE;

        for(int j=0;j<LEVEL_SIZE;j++) {
            xarr[j] = (j * arrsz);
            //     printf(" (x, = %d\n", (j*arrsz));
            yarr[j] = (j+1)*arrsz-1;
            //     printf(" y = %d\n", ((j+1)*arrsz-1));
        }

        //  for(int r=0;r<LEVEL_SIZE;r++) 
        //      printf(" (x, y) = %d,%d", xarr[r],yarr[r]);

        rowOfIntsX[k] = xarr;
        rowOfIntsY[k] = yarr;

    }

    // printf(" x y values  = \n");
    /*
       for(int k=1;k<NUM_ROWS;k++) {
       int *xg = rowOfIntsX[k];
       int *yg = rowOfIntsY[k];

       int lz = pow(2, k);
       printf(" row = %d", k);
       printf(" numvals = %d", lz);
       for(int g=0;g<lz;g++) {
       printf(" (x, y) = %i,%i", xg[g],yg[g]);
       }
       printf(" , ");
       printf(" \n");
       }
     */

    //    printf(" \n");
    // int pow21 = log2(N);

    //a row 0 = row1 and row8 = 512. we start with row 7 as buildtree 
    // is only until 2x2  e.g (0-3), (4-7) (384-387) etc.


    // Here is how we plan to do our dft. Data for row N depends on data from row N/2
    // As we are doing radix 2 dft, our data is in vectors and each row of buildTree corresponds to 1 row of 
    // of input record. The btree therefore is a array of records. The m_data is a pointer *** or in other words 
    // a pointer to a rows of records 1 to M. The m_rows parameter tells us the number of rows to be processed. The m_cols
    // should be a power of 2. we will first do our DFT in single thread without any locking and introduce
    // threads, locking etc. later. We will queue up as many rows as possible 5-6 at a time and process them 
    // concurrently :-) in a single thread. We will also do our DFT in place and modify the input array. The interface will document 
    // this explicitly that the input will be transformed in place. 

    int NUM_ROWS = 5;

    bflyPtr = bfly2;

    cbfunc = callback_func;

   
    _twProdFactors = malloc(sizeof(double _Complex) * NUM_ROWS);

    int batch_size = LEVEL_SIZE / 2;
    int LEVEL_END = 2;

    int batch_num = 0;
    int start_index = batch_num * batch_size;
    int record_num = 0;

    bptr_t btptr;

    btptr.opts = (RECURSION & MATCHING & SORT_ASC & EVENODD);

    btptr.batch_size = batch_size;
    btptr.batch_num = batch_num;
    btptr.level_size = LEVEL_SIZE;
    btptr.start_index = start_index;
    btptr.record_num = record_num;
    btptr.num_records = m_cols;
    btptr.level_end = LEVEL_END;
    btptr.base_radix = 2;

    register_func("do_bfly2", btptr, bflyPtr, cbfunc, imgPtr, m_rows, m_cols);

    for(int nx=0;nx<m_rows;nx+=NUM_ROWS) {

            int LEVEL_START = 8;
            int lz = pow(2, LEVEL_START);  //pow(2, (k));

            int xwid, ywid;

            xwid = ywid = m_size/128; // 4

            xarr = rowOfIntsX[lz];
            yarr = rowOfIntsY[lz];

            for(int x=0;x<NUM_ROWS;x++) 
                _twProdFactors[x] = malloc(sizeof(double _Complex) * lz/2);

            // we divide the 256 items of level 8 thus
            //  sets of 1 even amd 1 odd x[k] and x[k+N/2] 
            // this way same thread will process x[k] and x[k+N/2] , x[k+1] and x[k + N/2 + 1] and
            // and reuse the twiddle factor calculated

            // for the 256 items , it is thus  enough to process 128 items
            //  with 1 thread in effect
            // do_bfly2(xarr, yarr, lz, 256, j, nx);
            // or we can do in 2 batches each of size 128
            //   for(int i=0;i<2;i++) {
            //      do_bfly2(xarr, yarr, lz, 128, j, nx);
            //   }
            // of 4 batches each of size 64
            //   for(int i=0;i<4;i++) {
            //      do_bfly2(xarr, yarr, lz, 64, j, nx);
            //   } 
            // etc.

            
            // single batcch
            int batch_size = lz / 2;
            int LEVEL_END = 2;

            int batch_num = 0;
            int start = batch_num * batch_size;
            do_bfly2(lz, batch_size, batch_num, start, nx, LEVEL_START, LEVEL_END); 

            //do_bfly2(lz, 64, 0, nx); 
            //do_bfly2(lz, 64, 1, nx); 
                    //for(int j=0;j<BATCH_SIZE_EVEN;j++) 
                    //    do_bfly2(rowOfIntsX, rowOfIntsY, lz, batch_size, j); 

  }

}


void callback_func() {

}

void do_bfly2(int lz, int batch_size, int batch_num, int start_index, int record_num, int level, int level_end) {

    double _Complex d1,d2;
    while(batch_size>level_end) {
        int batch_sz = batch_size/2;

        int btnum = (batch_num + 1) * 2;  //64:2,3   32:6,7  8,9   16:14,15  16,17  18,19  20,21   30,31  32,33 34,35, i36,37  38,39 40,41  62,78 etc

        int div2 = batch_num/2;   // 6/2= 3 7/2 =3   8/2=4  9/2=4
        int rem2 = batch_num%2;   // 0        1         0     1
                                  // 14/2 = 7 15/2=7  16/2=8 17/2=8 18/2=9 19/2=9 20/2=10  21/2=10
                                  //  0        1        0      1      0      1       0         1
                                   // 30/2 = 15 31/2=15  32
    

        start_index = btnum*batch_sz;
        do_bfly2(lz, batch_sz, btnum, start_index, record_num, level, level_end);
        do_bfly2(lz, batch_sz, btnum+1, start_index+batch_sz, record_num, level, level_end);

    }

        int xarr[lz];
        int yarr[lz];

        xarr[lz] = rowOfIntsX[level][start_index]; 
        yarr[lz] = rowOfIntsY[level][start_index]; 
 
        int x1 = xarr[start_index];
        int y1 = yarr[start_index];

        int x2 = xarr[start_index+1];
        int y2 = yarr[start_index+1];

        int x3 = xarr[start_index+lz/2];
        int y3 = yarr[start_index+lz/2];

        int x4 = xarr[start_index+lz/2+1];
        int y4 = yarr[start_index+lz/2+1];

        // single atomic unit to be called as such
        d1 = bfly2(x1, y1, x2, y2, start_index, record_num);
        d2 = bfly3(x3, y3, x4, y4, start_index+lz/4, record_num);

        BFlyNode bflynode;

        bflynode.d1 = d1;
        bflynode.d2 = d2;

        return d2;

}


double _Complex bfly2(int x1, int y1, int x2, int y2, int num, int record_num) {

    double _Complex twfac = get_twiddle(num);
    double d1 = imgPtr[record_num][x1] * imgPtr[record_num][y2];
    double d2 = imgPtr[record_num][x2] * imgPtr[record_num][y1];

    _twProdFactors[record_num][num] = twfac * d2;
    double _Complex d3 = d1 + _twProdFactors[record_num][num];

    return d3;
}

double _Complex bfly3(int x1, int y1, int x2, int y2, int num, int record_num) {

    double _Complex twfac = get_twiddle(num);
    double d1 = imgPtr[record_num][x1] * imgPtr[record_num][y2];
    double d2 = imgPtr[record_num][x2] * imgPtr[record_num][y1];

    double _Complex d3 = d1 - _twProdFactors[0][num];

    return d3;
}

double _Complex get_twiddle(int num) {

    if(num <0 || num > 127) {
        std::cout << " num out of bounds " << std::endl;
        return NULL;
    }

    double _Complex z1 = cosines[num] + sines[num] * I;

    return z1;


}


int get_log2(int size) {

    std::cout << " getlog2 size   = " << size << std::endl;
    int logof2 = 0;
    for(int i=0;i<NumEntriesLogOfSizes;i++) {
        int *lognum = LogOfSizes[i];
        int lgnum = lognum[0];

        if(lgnum == size) 
            logof2 = i; 

    }
    std::cout << " getlog2   = " << logof2 << std::endl;
    return logof2+1;
}


void buildDFTree(struct DFTNode *rootNode, int step_count, int step_id) {

    bool treeFinished = false;
    //      std::cout << " BUILD DFT TREE   = " << m_rows << std::endl;
    do {
        buildTree2(rootNode, step_count, step_id, "LEFT");



        buildTree2(rootNode, step_count, step_id, "RIGHT");


        /*               
                         std::cout << " CALLING BT RIGHT on LSUBNODE of ROOTNODE ID  = " << rootNode->sub_nodes[0]->node_id << std::endl;

                         std::cout << "  LSUBNODE x, y  = " << rootNode->sub_nodes[0]->x << ", "  << rootNode->sub_nodes[0]->y <<  std::endl;

                         buildTree(rootNode->sub_nodes[0], step_count, step_id, "RIGHTLEFT");


        //   std::cout << " CALLING BT LEFT on RSUBNODE of ROOTNODE ID  = " << rootNode->sub_nodes[1]->node_id << std::endl;

        //  std::cout << "  RSUBNODE x, y  = " << rootNode->sub_nodes[1]->x << ", "  << rootNode->sub_nodes[1]->y <<  std::endl;

        //             buildTree(rootNode->sub_nodes[1], step_count, step_id, "LEFT");

         */ 

        treeFinished = true;

    } while(!treeFinished);

}

void buildDFTreeAlt(struct DFTNode *rootNode, int step_count, int step_id) {

    bool treeFinished = false;
    do {
        buildTree(rootNode, step_count, step_id, "LEFT");



        buildTree(rootNode, step_count, step_id, "RIGHT");



        std::cout << " CALLING BT RIGHT on LSUBNODE of ROOTNODE ID  = " << rootNode->sub_nodes[0]->node_id << std::endl;

        std::cout << "  LSUBNODE x, y  = " << rootNode->sub_nodes[0]->x << ", "  << rootNode->sub_nodes[0]->y <<  std::endl;

        buildTree(rootNode->sub_nodes[0], step_count, step_id, "RIGHTLEFT");


        //   std::cout << " CALLING BT LEFT on RSUBNODE of ROOTNODE ID  = " << rootNode->sub_nodes[1]->node_id << std::endl;

        //  std::cout << "  RSUBNODE x, y  = " << rootNode->sub_nodes[1]->x << ", "  << rootNode->sub_nodes[1]->y <<  std::endl;

        //             buildTree(rootNode->sub_nodes[1], step_count, step_id, "LEFT");



        treeFinished = true;

    } while(!treeFinished);

}

void buildTree(struct DFTNode *rootNode, int step_count, int step_id, std::string direc) {

    step_count = rootNode->step_count;

    int pow21 = pow(2, step_count);
    double N2 = N * 1/pow21;
    struct DFTNode *dfnodes;

    std::cout << step_count << std::endl;

    int NN = (int) N2;

    std::cout << " ENTERING BT ROOTNODE ID  = " << rootNode->node_id << std::endl;
    if(N2 < 1)
        NN = 0;

    if(NN == 2) {
        std::cout << " NN 0 . returning...= " << NN << std::endl;
        return;
    }


    int num_subnodes = pow21;

    std::cout << " BT stepcount = " << step_count << std::endl;
    std::cout << " BT numsubnodes = " << num_subnodes << std::endl;


    /*
       step = 1;
       num_subnodes = 2

node1 := createNode 
node2 := createNode 

buildTree(node1, step=2)
buildTree(node2, step=2)

root->node1, node2


step =2
num_subnodes = 4


node11 := createNode 
node12 := createNode 

node1->node11, node12


node21 := createNode 
node22 := createNode 


node2->node21, node22
     */


    bool isLeft = false;
    bool isRight = false;
    bool isRightLeft = false;
    bool isLeftRight = false;;
    DFTNode *nodeptr;
    int step_ctr = step_count + 1;

    int q = 0;
    if(strcmp(direc.c_str(), "LEFT") == 0) {
        q = 0;
        isLeft = true;
    } else if(strcmp(direc.c_str(), "RIGHT") == 0) {
        q = 1;
        isRight = true;
    } else if(strcmp(direc.c_str(), "LEFTRIGHT") == 0) {
        q = 0;
        isLeftRight = true;

    } else  if(strcmp(direc.c_str(), "RIGHTLEFT") == 0) {
        q = 0;
        isRightLeft = true;

    }

    //  for(int q=0;q<1;q++) {

    std::cout << " BT q = " << q << std::endl;
    if(q == 0)
        std::cout << " BT LEFT ===== " << direc << std::endl;
    else
        std::cout << " BT RIGHT ===== " << direc << std::endl;

    std::cout << " starts = " << rootNode->x << std::endl;
    std::cout << "ends = " << rootNode->y << std::endl;

    std::cout << " BT step_id " << step_id << std::endl;
    std::cout << " BT N/pow21 " << N/pow21 << std::endl;
    std::cout << " BT isLeft =  " << isLeft << std::endl;
    std::cout << " BT isRight = " << isRight << std::endl;
    std::cout << " BT isRightLeft =  " << isRightLeft << std::endl;
    std::cout << " BT isLeftRight = " << isLeftRight << std::endl;

    int xoffset = 0;
    int xstart = rootNode->x;
    int xend = rootNode->y;
    if(isRight) { // direc == right , q == 1  {
        // xoffset = (q + num_subnodes/2-1)*(N/pow21);
        xoffset = N/2;

        if(xend < N/2)
            if( ((xend+1) % 4) == 0) {
                std::cout << " xofseet = xend+1 mod 4  " << ((xend+1) % 4)<< std::endl;
                xoffset = (xend+1)/2;
            } else
                xoffset = xstart;

        if(xoffset < xstart)
            xoffset = xstart;

    } else if(isLeft) { // q = 0 {
        xoffset = (q + num_subnodes/2-1)*(N/pow21);
    } else if(isRightLeft) {
        xoffset = q;
    }

    std::cout << " BT xoffset " << xoffset << std::endl;
    xstart = 0 + xoffset; 
    xend = (N/pow21)-1 + xoffset; 

    std::cout << " BT xstart = " << xstart << std::endl;
    std::cout << " BT xend = " << xend << std::endl;

    dfnodes = new DFTNode[1];
    dfnodes[0].x = xstart;
    dfnodes[0].y = xend;
    dfnodes[0].step_id = step_id;
    dfnodes[0].step_count = step_ctr;
    dfnodes[0].num_siblings = num_subnodes; // should be > num_subnodes
    dfnodes[0].node_id = std::string("DF" + itoa((step_count), 10) + "_" + itoa(xstart, 10) + "_" + itoa(q, 10));
    dfnodes[0].parent = rootNode;

    nodeptr = &dfnodes[0];

    //      }

    if(q == 1) ++step_id;

    buildTree(nodeptr, step_count, step_id, direc); 

    //   }

    //      if(isLeft) { 
    std::cout << " linking node = " << dfnodes[0].node_id  <<  " to " << rootNode->node_id << std::endl;
    rootNode->sub_nodes[q] = &dfnodes[0];        
    //        } else if(isRight) {
    //            std::cout << " linking node = " << dfnodes[0].node_id  <<  " to " << rootNode->node_id << std::endl;
    //            rootNode->sub_nodes[1] = &dfnodes[1];        
    //        }


    std::cout << " isRightLeft = " << isRightLeft  << std::endl;
    if(isRightLeft) {

        DFTNode * currNode = rootNode;

        std::cout << " currnode id = " << currNode->node_id  << std::endl;

        while(currNode != NULL) {
            std::cout << " linking right nodes to left node = " << currNode->node_id  << std::endl;

            buildTree(currNode, step_count, step_id, "RIGHT");

            currNode = currNode->parent;
        }

    }

}


void buildTree2(struct DFTNode *rootNode, int step_count, int step_id, std::string direc) {

    N = m_cols;

    int pow21 = pow(2,step_count);

    //     int pow21 = pow(2, step_count);
    int N2 = N * 1 / pow21;
    struct DFTNode *dfnodes;

    //   std::cout << step_count << std::endl;


    int num_subnodes = pow21;

    /*
       std::cout << " ENTERING BT ROOTNODE ID  = " << rootNode->node_id << std::endl;
       std::cout << " direc  = " << direc << std::endl;
       std::cout << " N/pow21  = " << N/pow21 << std::endl;
       std::cout << " BT stepcount = " << step_count << std::endl;
       std::cout << " BT numsubnodes = " << num_subnodes << std::endl;
       std::cout << " BT step_id " << step_id << std::endl;
       std::cout << " BT xstart " << rootNode->x << std::endl;
       std::cout << " BT xend " << rootNode->y << std::endl;
       std::cout << " N2 " << N2 << std::endl;
     */

    if(N2 <= 1) {
        //       std::cout << " NN 1 . returning...= " << N2 << std::endl;

        //xstart,xend
        //   rootNode->m_data = imgPtr + (int) rootNode->x/2;
        //   rootNode->num_rows=2;
        //   rootNode->num_cols=2;

        //    std::cout << " NN 1 = " << std::endl;

        //    std::cout << " img x, y = " << rootNode->m_data[0][0] << ", " << rootNode->m_data[0][1] << std::endl;
        //    std::cout << " img x2, y2  = " << rootNode->m_data[1][0] << ", " << rootNode->m_data[1][1] <<  std::endl;

        //     std::cout << " from img x, y = " << imgPtr[(int) rootNode->x/2][0] << ", " << imgPtr[(int) rootNode->x/2+1][1] << std::endl;
        //   std::cout << " from img x2, y2  = " << imgPtr[(10+ (int) rootNode->x/2)][0] << ", " << imgPtr[(10+ (int) rootNode->x/2)+1][1] <<  std::endl;

        return;
    }


    DFTNode *nodeptr1, *nodeptr2;

    int xoffset = 0;


    // build 0-255 branch
    int q = 0;

    int y = step_id % 2;
    int fyk = (int) step_id / 2;
    //   xoffset = (N/pow21 + num_subnodes/2)*(N/pow21);

    //8-15 = 8-11

    int xstart = rootNode->x;
    int xend = rootNode->y; 

    xoffset = xstart;

    //      std::cout << " BT xoffset " << xoffset << std::endl;


    xstart = 0 + xoffset; 
    // xend = (N/pow21)-1 + xoffset; 

    xend = xstart + (xend - xstart+1)/2 -1;
    //    std::cout << " BT xstart = " << xstart << std::endl;
    //    std::cout << " BT xend = " << xend << std::endl;

    dfnodes = new DFTNode[1];
    dfnodes[0].x = xstart;
    dfnodes[0].y = xend;
    dfnodes[0].step_id = step_id;
    dfnodes[0].step_count = num_subnodes;
    dfnodes[0].node_id = std::string("DF" + itoa((step_count), 10) + "_" + itoa(q, 10));
    dfnodes[0].sub_nodes[0] = NULL;
    dfnodes[0].sub_nodes[1] = NULL;

    dfnodes[0].m_data = imgPtr;
    dfnodes[0].num_rows = m_rows;
    dfnodes[0].num_cols = m_cols;

    nodeptr1 = &dfnodes[0];


    buildTree2(nodeptr1, ++step_count, step_id+1, "LEFT"); 

    //     std::cout << " linking node = " << dfnodes[0].node_id  <<  " to " << rootNode->node_id << std::endl;
    rootNode->sub_nodes[0] = nodeptr1;        

    step_count--;

    // build 256-511 branch
    q = 1;

    //    std::cout << " BT root xstart " << rootNode->x << std::endl;
    //    std::cout << " BT root xend " << rootNode->y << std::endl;
    xstart = rootNode->x;
    xend = rootNode->y;

    //    std::cout << " BT PART II 256-511 branch " << std::endl;

    //    std::cout << " BT xstart " << xstart << std::endl;
    //    std::cout << " BT xend " << xend << std::endl;

    xoffset = (xend - xstart+1)/ 2;
    // xoffset = (q + num_subnodes/2-1)*(N/pow21);

    //    std::cout << " BT xoffset " << xoffset << std::endl;
    xstart = xstart + xoffset; 
    xend = xend; 

    //    std::cout << " BT xstart = " << xstart << std::endl;
    //    std::cout << " BT xend = " << xend << std::endl;

    dfnodes = new DFTNode[1];
    dfnodes[0].x = xstart;
    dfnodes[0].y = xend;
    dfnodes[0].step_id = step_id;
    dfnodes[0].step_count = num_subnodes;
    dfnodes[0].node_id = std::string("DF" + itoa((step_count), 10) + "_" + itoa(q, 10));
    dfnodes[0].sub_nodes[0] = NULL;
    dfnodes[0].sub_nodes[1] = NULL;

    dfnodes[0].m_data = imgPtr;
    dfnodes[0].num_rows = m_rows;
    dfnodes[0].num_cols = m_cols;

    nodeptr2 = &dfnodes[0];

    buildTree2(nodeptr2, ++step_count, step_id, "LEFT"); 

    //   std::cout << " linking node = " << nodeptr2->node_id  <<  " to " << rootNode->node_id << std::endl;
    rootNode->sub_nodes[1] = nodeptr2;        


    step_count--; 


}

void buildTree4ary(struct DFTNode *rootNode, int step_count, int step_id) {


    int pow21 = pow(2,step_count+1); // 4

    int sz = N/4; // 128

    int num_subnodes = 4;
    DFTNode *dfnodes;
    DFTNode *nodeptr2;
    dfnodes = new DFTNode[1];
    dfnodes[0].x = 0;
    dfnodes[0].y = sz-1;
    dfnodes[0].x2 = 0;
    dfnodes[0].y2 = sz-1;
    dfnodes[0].step_id = step_id;
    dfnodes[0].step_count = num_subnodes;
    dfnodes[0].node_id = std::string("DF_TL_" +  itoa((step_count+1), 10) + "_" + itoa(step_id, 10));
    dfnodes[0].sub_nodes[0] = NULL;
    dfnodes[0].sub_nodes[1] = NULL;
    dfnodes[0].sub_nodes[2] = NULL;
    dfnodes[0].sub_nodes[3] = NULL;

    dfnodes[0].m_data = imgPtr;
    dfnodes[0].num_rows = m_rows;
    dfnodes[0].num_cols = m_cols;

    nodeptr2 = &dfnodes[0];
    buildTreeTL(nodeptr2, step_count+2, step_id);

    rootNode->sub_nodes[0] = nodeptr2;

    dfnodes = new DFTNode[1];
    dfnodes[0].x = sz;
    dfnodes[0].y = 2*sz-1;
    dfnodes[0].x2 = 0;
    dfnodes[0].y2 = sz-1;
    dfnodes[0].step_id = step_id;
    dfnodes[0].step_count = num_subnodes;
    dfnodes[0].node_id = std::string("DF_TR_" +  itoa((step_count+2), 10) + "_" + itoa(step_id, 10));
    dfnodes[0].sub_nodes[0] = NULL;
    dfnodes[0].sub_nodes[1] = NULL;
    dfnodes[0].sub_nodes[2] = NULL;
    dfnodes[0].sub_nodes[3] = NULL;

    dfnodes[0].m_data = imgPtr;
    dfnodes[0].num_rows = m_rows;
    dfnodes[0].num_cols = m_cols;
    buildTreeTR(nodeptr2, step_count+2, step_id);

    buildTreeLL(nodeptr2, step_count+2, step_id);

    buildTreeLR(nodeptr2, step_count+2, step_id);

}

void buildTreeTL(struct DFTNode *nodeptr2, int step_count, int step_id) {}
void buildTreeTR(struct DFTNode *nodeptr2, int step_count, int step_id) {}
void buildTreeLL(struct DFTNode *nodeptr2, int step_count, int step_id) {}
void buildTreeLR(struct DFTNode *nodeptr2, int step_count, int step_id) {}





/**
 * C++ version 0.4 std::string style "itoa":
 * Contributions from Stuart Lowe, Ray-Yuan Sheu,

 * Rodrigo de Salvo Braz, Luc Gallant, John Maloney
 * and Brian Hunt
 */
std::string itoa(int value, int base) {

    std::string buf;

    // check that the base if valid
    if (base < 2 || base > 16) return buf;

    enum { kMaxDigits = 35 };
    buf.reserve( kMaxDigits ); // Pre-allocate enough space.


    int quotient = value;

    // Translating number to string with base:
    do {
        buf += "0123456789abcdef"[ std::abs( quotient % base ) ];
        quotient /= base;
    } while ( quotient );

    // Append the negative sign
    if ( value < 0) buf += '-';

    std::reverse( buf.begin(), buf.end() );
    return buf;
}



/*
/// Do the operation new_image(i,j) = alpha*image(i,j) + beta
for( int y = 0; y < image.rows; y++ )
{ 
for( int x = 0; x < image.cols; x++ )
{ 
int z = image.rows - y;

if(x == y) {
if(isPowerOf2(z)) {

int zbase = (int) math.log(x, 2);
xy_stack.push(zbase);


}
}  

}
} 

double dft2 = 0;
while(!xy_stack.empty()) {

int z = xy_stack.pop();

if(z == 1) {
// even
double dft2 = 0;
while(!xy_stack.empty()) {

int z = xy_stack.pop();

if(z == 1) {
// even
int x0 = image.at<Vec3b>(z, z)[0]
int x1 = image.at<Vec3b>(z+1, z)[0]
// odd
int y0 = image.at<Vec3b>(z+0, z+1)[0]
iint y1 = image.at<Vec3b>(z+1, z+1)[0]

// even + (twiddle) * odd

fac = get_twiddle();

dft2 = (x0+x1) + fac * (y0+y1);

} 
else {

int div = z*2; //  for z=2, the size is 2*z = 4
int NN = N/div; //  for N=256, we want to divide by 64

int sumeven = 0;
for(int yy=0;yy<NN-1;yy++) {

for(int xx=0;xx<NN-1;xx++) {

int y2 = image.at<Vec3b>(yy, xx)[0]

sumeven += y2;

}
}         

int sumodd = 0;
for(int yyodd=NN;yyodd<2*NN-1;yyodd++) {

for(int xxodd=NN;xxodd<2*NN-1;xxodd++) {

int y2 = image.at<Vec3b>(yyodd, xxodd)[0]

sumodd += y2;

}
}         

fac = get_twiddle();

}


}
*/


/*

   double bfly() {

   dft2even(); 
   dft2odd(); 

   add_twiddle();

   return

   }

 */
