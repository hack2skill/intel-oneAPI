#include "bfly.h"

#define RECURSION 1
#define MATCHING 2
#define CALLBACK 3
#define SORT_ASC 4
#define SORT_DESC 5
#define EVENODD 6

int ** rowOfIntsX;
int ** rowOfIntsY;
double _Complex **twProdFactors;


//void (*func_ptrs[3])(int x, double d);

int iptr;
int size;

struct start_index_t {

    int start_index1;
    int start_index2;

};

struct iptr_t {

   int iptr;
   int size;
   bool multi;

};

struct result_t {

};

struct bptr_t {

    unsigned int level_size;
    unsigned int level;
    unsigned int batch_size;
    unsigned int batch_num;
    unsigned int start_index;
    unsigned int num_records;
    unsigned int record_num;
    unsigned int level_start;
    unsigned int level_end;

    unsigned int base_radix = 2; //4

    bool use_threads;
    bool use_pthreads;
    bool use_gthreads;

    unsigned int opts;
};


bptr_t mybptr;


typedef struct client_info_t {


   char *client_id;
   int c_index;
 
   double **m_data;
   int m_rows;
   int m_cols;

   bptr_t *p_bptr;

} client_info_t;

enum EXECUTION_STRATEGY {
    RADIX2_QUICK,
    RADIX2_QUEUE,
    RADIX4_SUM,
    RADIX4_TWIDDLE
};

struct func_info_t {

   char * fid;
   void (*fp)();

   enum EXECUTION_STRATEGY exec_strateg;

   bptr_t *f_pbptr;

   BFlyNode *bflynode_ptr;

   client_info_t *c_info;

   int start_row;
   int end_row;
} func_info_t;


struct iptr_t iptr_info[3];

void register_func(char *name, bptr_t bptr, void (*fp)(), void (*cbfunc)(), double **dblptr, int m_rows, int m_cols);
void register_func_multi(char *name, bptr_t bptr, void (*fp1)(), void (*fp)(), void (*cbfunc)());

int rand_interval(int rlow, int rmax);
const char *generate_unique_id();
void fft();
void *run4(void *p);
void radix2_dft_quick(struct func_info_t *fp, int rnum);
void *progress_dft(void *t);
double _Complex bfly2(int i1, int i2, int i3, int i4, int i5, int i6);
double _Complex bfly3(int i1, int i2, int i3, int i4, int i5, int i6);
double _Complex get_twiddle(int i1);
void update_state(struct func_info_t *f);
struct result_t results();

typedef enum {
    CHAR,
    INT,
    FLOAT,
    DOUBLE
} TYPE;


void foo(TYPE t, void** x, int len);
/*
    switch(t){
        case CHAR:
            (char*)x;
            break;
        case INT:
            (int*)x;
            break;
         ...
    }
 }

*/
double cosines [] =
{
    -0.999924706,-0.999322425,-0.998118224,-0.99631283,-0.993907329,-0.990903171,-0.987302166,-0.983106481,-0.978318645,-0.972941541,-0.966978408,-0.960432838,-0.953308773,-0.945610504,-0.937342669,-0.928510247,-0.919118557,-0.909173258,-0.898680339,-0.887646121,-0.876077249,-0.863980693,-0.851363737,-0.838233982,-0.824599336,-0.810468011,-0.795848519,-0.780749667,-0.765180548,-0.749150539,-0.732669298,-0.715746749,-0.698393087,-0.680618764,-0.662434486,-0.643851205,-0.624880116,-0.605532644,-0.585820443,-0.565755387,-0.545349562,-0.524615257,-0.503564963,-0.482211357,-0.460567303,-0.438645837,-0.416460162,-0.394023642,-0.371349791,-0.348452266,-0.325344858,-0.302041487,-0.278556188,-0.254903107,-0.231096491,-0.207150679,-0.183080095,-0.158899236,-0.134622669,-0.110265014,-0.085840944,-0.06136517,-0.036852433,-0.0123175,0.012224853,0.036759842,0.06127269,0.085748632,0.110172925,0.134530858,0.158807759,0.182989006,0.207060034,0.231006344,0.254813513,0.2784672,0.30195316,0.325257244,0.348365418,0.371263761,0.393938482,0.416375924,0.438562571,0.460485059,0.482130186,0.503484912,0.524536375,0.545271896,0.565678985,0.585745351,0.605458906,0.624807776,0.643780308,0.662365074,0.680550879,0.698326771,0.71568204,0.732606236,0.749089162,0.765120893,0.78069177,0.795792415,0.810413733,0.824546916,0.838183453,0.851315129,0.863934035,0.876032571,0.887603448,0.898639697,0.909134672,0.91908205,0.92847584,0.937310383,0.94558036,0.953280788,0.960407029,0.96695479,0.972920129,0.978299452,0.983089518,0.987287443,0.990890698,0.993897113,0.996304876,0.998112538,0.99931901,0.999923565
};

double sines [] =
{
    -0.0122,-0.0368,-0.0613,-0.0857,-0.1102,-0.1345,-0.1588,-0.183,-0.207,-0.231,-0.254,-0.278,-0.301,-0.325,-0.348,-0.371,-0.393,-0.416,-0.438,-0.46,-0.482,-0.503,-0.524,-0.545,-0.565,-0.585,-0.605,-0.624,-0.643,-0.662,-0.68,-0.698,-0.715,-0.732,-0.749,-0.765,-0.78,-0.795,-0.81,-0.824,-0.838,-0.851,-0.863,-0.876,-0.887,-0.898,-0.909,-0.919,-0.928,-0.937,-0.945,-0.953,-0.96,-0.966,-0.972,-0.978,-0.983,-0.987,-0.99,-0.993,-0.996,-0.998,-0.999,-0.999,-0.999,-0.999,-0.998,-0.996,-0.993,-0.99,-0.987,-0.983,-0.978,-0.972,-0.967,-0.96,-0.953,-0.945,-0.937,-0.928,-0.919,-0.909,-0.898,-0.887,-0.876,-0.864,-0.851,-0.838,-0.824,-0.81,-0.795,-0.78,-0.765,-0.749,-0.732,-0.715,-0.698,-0.68,-0.662,-0.643,-0.624,-0.605,-0.585,-0.565,-0.545,-0.524,-0.503,-0.482,-0.46,-0.438,-0.416,-0.394,-0.371,-0.348,-0.325,-0.302,-0.278,-0.255,-0.231,-0.207,-0.183,-0.159,-0.134,-0.11,-0.085,-0.061,-0.036,-0.012
};

//char chars[62] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW XYZ1234567890".ToCharArray();
const char *chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW XYZ1234567890";
