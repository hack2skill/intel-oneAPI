#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <pthread.h>
#include <time.h>
#include <math.h>

#include "hashtable.h"
#include "sglib.h"
#include "thpool.h"
#include "array.h"
#include "registry.h"
#include "pipe.h"


HashTable *func_table, *cacheTbl;
double **m_data;
int m_rows, m_cols, LEVEL_SIZE;

Array *client_data;

Array *counters;

int c_index;
int next_thread_id = 0;
//int NUM_THREADS=50;
//pthread_t thread[NUM_THREADS];
//all important pointer that this library uses to identify
// client data is for which client. requires synchronization
// this library has considerably assumed significance and is now meant
// to be a general purpose library meant for multiple clients and employs a
// sqlite daatabase to load/store data for when the routines are to be executed
// including a scheduler, a variety of high level routines, and strategy for
// executing them, all this while keeping the size exceedingly low and functionality clear

int stage_kerns[][3] = {
                     { 2, 4, 8 },
                     { 4, 8, 16 },
                     { 8, 16, 32 },
                     { 16, 32, 64 },
                     { 32, 64, 128 },
                     { 64, 128, 256 },
                     { 128, 256, 512 }
                   }; // Works

int layerMask4[] = { 1, 0, 1, 0 };
int layerMask8[] = { 1, 0, 1, 0, 1, 0, 1, 0 };

int layerMask[][] = 
             {
                {},
                {},
                {},
                layerMask4,
                {},
                {},
                {},
                layerMask8
             };


__thread int TLS_c_index;
__thread struct func_info_t * TLS_func_info;

pthread_mutex_t finfo_mutex;
pthread_cond_t finfo_threshold_cv;
bool allworkdone = true;
bool dft_in_progress = false;

// some sglib data structures

struct ilist {
    struct func_info_t *fi;
    struct ilist *next_ptr;
};


#define ILIST_COMPARATOR(e1, e2) (e1->fi->f_pbptr->record_num - e2->fi->f_pbptr->record_num) 

#define ILIST_COLUMN_COMPARATOR(e1, e2) (e1->fi->f_pbptr->start_index - e2->fi->f_pbptr->start_index) 

Array *row_array;

struct ilist *l;
struct ilist *the_list;


threadpool thpool, thpool_pdft;
double _Complex **dfactors;

int KERNEL_SIZE_FOR_STAGE(int stage_num)  {
       for(int mj=0;mj<7;mj++) if(stage_kerns[mj]==stage_num) return stage_kerns[mj][rand()%2];
}

int KERNEL_SIZE_MAX_FOR_STAGE(int stage_num) {
    for(int mj=0;mj<7;mj++) if(stage_kerns[mj]==stage_num) return stage_kerns[mj][2];
}

int register_func(const char * generic_name, bptr_t bptr, void (*funcPtr)(), double **imgPtr, int rows, int cols) {

    m_cols = cols;
    m_rows = rows;
    m_data = imgPtr;
 
   
    if(func_table == NULL) {
        if (hashtable_new(&func_table) != CC_OK) {
           printf(" error registering\n");
           return;
        }

        if (array_new(&counters) != CC_OK) {
        }

        if (array_new(&client_data) != CC_OK) {
        }

        /*
        int NUMPOOLTHREADS=8;
        thpool = thpool_init(NUMPOOLTHREADS);
        thpool_pause(thpool)

        NUM_ROWS=64;
        dfactors = malloc(sizeof(double *)*NUM_ROWS):
        for(int ij=0;ij<NUMPOOLTHREADS;ij++) {
            array_slice asl;
            asl.slice = dfactors;
            asl.start_row = ij;
            asl.end_row = ij+NUM_ROWS;
            thpool_add_work(thpool, (void*)run_dft_4, &asl);
        }
        */
        // we will use a thread pool for rows 
        // and a pipe for dft layers. There will be a pipe for 
        // each row.  The thread pool for rows will terminate 
        // and return to pool after computing level 2 DFTs.
        // these threads will subsequently become pipe threads 
        // for the correspoding rows. another thread pool with 2,4 threads 
        // will be created for loading the relusts of level 2 dft into 
        // the double array

        int NUM_ROWS=64;
        thpool = thpool_init(NUM_ROWS);
	dfactors = malloc(sizeof(double _Complex *)*m_cols);

        for(int d=0;d<cols;d++) 
	    dfactors[d] = malloc(sizeof(double _Complex)*m_cols/2);

        for(int ij=0;ij<cols;ij+=8) {
            struct func_info_t ft;
            ft.fid = "run4";
            ft.fp = run4;
            ft.start_row = ij;
            ft.end_row = ij+7;
            thpool_add_work(thpool, (void*)run4, &ft);
        }
        thpool_pause(thpool);

        thpool_pdft = thpool_init(2);
        thpool_pause(thpool_pdft);
        thpool_add_work(thpool_pdft, (void*)progress_dft, (void *) 2);

         pipe_t my_pipe;
         
         pipe_create (&my_pipe, 8, thpool);
         //pipe starts kicks off the pipeline
         //    pipe_start (&my_pipe, value);


        // counters = malloc(sizeof(int)*10); 
    }

    if(cacheTbl == NULL) {
        if (hashtable_new(&cacheTbl) != CC_OK) {
           printf(" error caching\n");
           return;
        }
    }

   // Add key-value pair
    if (hashtable_add(func_table, generic_name, funcPtr) != CC_OK) {
         printf(" error registering\n");
         return;
    } 
   
   bptr_t *mybptr = malloc(sizeof(struct bptr_t)*1);

   mybptr->batch_size = bptr.batch_size;
   mybptr->batch_num = bptr.batch_num;
   mybptr->level_size = bptr.level_size;
   mybptr->level_start = bptr.level_start;
   mybptr->level_end = bptr.level_end;
   mybptr->start_index = bptr.start_index;
   mybptr->record_num = bptr.record_num;
   mybptr->num_records = bptr.num_records;
   
   LEVEL_SIZE = bptr.level_size;

   const char *id = generate_unique_id();

   size_t sz = array_size(counters);

   array_add(counters, sz+1);

   client_info_t cinfo;

   cinfo.client_id = id;
   cinfo.c_index = sz+1; 

   cinfo.p_bptr = mybptr;

   cinfo.m_data = imgPtr;
   cinfo.m_rows = rows;
   cinfo.m_cols = cols;
   
   array_add(client_data, &cinfo);

   if(hashtable_add(cacheTbl, generic_name, &cinfo) != CC_OK) {
       printf(" error caching\n");
       return;
   } 


}

bool noerrors = true;

int batch_size;
int batch_num;
int level_size;
int start_index;
int level_start;
int level_end;
int record_num;
int num_records;

enum EXECUTION_STRATEGY strategy;


void prepare() {

   strategy = RADIX2_QUICK;

   fft();

}

void begin_run() {

//  int *ctr = (int *) array_get_at(counters, TLS_c_index); 
//  array_replace_at(counters, *ctr++); 
}

/*
* client will supply the client Id and the name of the function to run
*/
void run(const char *client_id, char * func_name) {

           struct func_info_t ft[64];
           struct func_info_t *finfo_ptr;
           int c_index;
           client_info_t *cval;
           if (hashtable_get(cacheTbl, client_id, (void*) cval) == CC_OK) {
               client_id = cval->client_id; 
               c_index = cval->c_index;
           } else {
               ArrayIter ai;
               array_iter_init(&ai, client_data);

                client_info_t *next;
                while (array_iter_next(&ai, (void *) &next) != CC_ITER_END) {
                    if(next->client_id == client_id) {
                        client_id = next->client_id;
                        c_index = next->c_index;
                        break;
                    }
                }
           }

    if (hashtable_get(func_table, func_name, (void*) finfo_ptr) == CC_OK) {

        int r=0;
        for(int ij=0;ij<m_cols;ij+=8) {
            ft[r].fid = "run4";
            ft[r].fp = run4;
            ft[r].start_row = ij;
            ft[r].end_row = ij+7;
            thpool_add_work(thpool, (void*)run4, &ft[r++]);
        }

        thpool_resume(thpool);
    }

    
     /*
    HashTableIter hti;
    hashtable_iter_init(&hti, func_table);

    client_info_t *cinfo;
    TableEntry *entry;
    while (hashtable_iter_next(&hti, &entry) != CC_ITER_END) {
        if (strcmp(entry->key, fid) == 0) {
        // safely remove an entry from the table and ignore the removed value
        //    hashtable_iter_remove(&hti, NULL);

           void *cval;
           void (*ptr_func)();
           if (hashtable_get(func_table, fid, (void*) cval) == CC_OK)
                ptr_func = cval;
           } else {
               ArrayIter ai;
               array_iter_init(&ai, client_data);

                void *next;
                while (array_iter_next(&ai, &next) != CC_ITER_END) {
                   cinfo = next;
                }
           }

           void (*ptr_func)() = &hti;

        //   run4(fid, ptr_func, execution_strategy);
     */

         //  finfo_ptr->exec_strateg = execution_strategy;

           /*
           printf("Main: creating thread %ld\n", t);
           pthread_attr_t attr;
           pthread_attr_init(&attr);
           long t1="87";
           pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
           pthread_create(&thread[next_thread_id++], &attr, run4, (void *)&finfo); 
           pthread_create(&thread[next_thread_id++], &attr, progress_dft, (void *)t1); 
          */

           /* Free attribute and wait for the other threads */
           //pthread_attr_destroy(&attr);
           /* join can wait
           for(t=0; t<NUM_THREADS; t++) {
              rc = pthread_join(thread[t], &status);
              if (rc) {
                  printf("ERROR; return code from pthread_join() is %d\n", rc);
                  exit(-1);
             }
             printf("Main: completed join with thread %ld having a status of %ld\n",t,(long)status);
           }
           */


}

void end_run() {

//  int *ctr = (int *) array_get_at(counters, c_id); 
//  array_add_at(counters, *ctr--); 


}


result_t results() {
   result_t res1;
   return res1;
}


void unregister_func(const char *name) {

    hashtable_remove(func_table, name, NULL);

}

int pre_callback(const char *name) {

   //  ++counters[c_index];
     
}


void *run4(void * param) {

    struct func_info_t *finfo = param;

    client_info_t *cinfo = finfo->c_info;

    TLS_c_index = cinfo->c_index;

    thpool_resume(thpool_pdft);

    if(!noerrors) {
       printf(" errors found. run aborted\n");
       return;
    }

    if(strategy == RADIX2_QUICK) {
        prepare();

        dft_in_progress = true;
        the_list = NULL;

        int start_row = finfo->start_row;
        int end_row = finfo->end_row;

        for(int k=start_row;k<end_row;k++) {
           // send level 2 dft information
            int num_batches = 128; 
            for(int h=0;h<num_batches;h++) {

                bptr_t bptr;
                bptr.level_size = level_size;
                bptr.batch_size = batch_size;
                bptr.batch_num = batch_num;
                bptr.start_index = start_index;
                bptr.record_num = k;
                bptr.level_start = level_start;
                bptr.level_end = level_end;

                finfo->f_pbptr = &bptr;

                radix2_dft_quick(finfo, k);
            }
        }

    }


}

void  radix2_dft_quick(struct func_info_t *finfo, int record_num) {


       begin_run();

       double _Complex d1,d2;
       /*
       while(batch_size>level_end) {
           int batch_sz = batch_size/2;

           int btnum = (batch_num + 1) * 2;  

           //start_index = btnum*batch_sz;

           start_index_t sxt = get_start_index(btnum);

           bptr_t bptr1;
     
           bptr1.batch_size = batch_sz;
           bptr1.batch_num = btnum;
           bptr1.level_size = lz;
           bptr1.level_start = level;
           bptr1.level_end = level_end;
           bptr1.start_index = sxt.start_index1;
           bptr1.record_num = record_num;

           finfo->f_pbptr = &bptr1;
     
           d1 = radix2_dft_quick(finfo);

           int btnum2 = btnum+1;
           bptr_t bptr2;

           bptr2.batch_size = batch_sz;
           bptr2.batch_num = btnum;
           bptr2.level_size = lz;
           bptr2.level_start = level;
           bptr2.level_end = level_end;
           bptr2.start_index = sxt.start_index2;
           bptr2.record_num = record_num;

           finfo->f_pbptr = &bptr2;

           d2 = radix2_dft_quick(finfo);

      }
      */

      // 64: 2,3
      // 32: 6,7,8,9
      // 16: 14,15,16,17,18,19,20,21
      // 8 : 30, 45
      // 4 : 62 .. 93
      // 2: 126 .. 189
      
      level_size = 256;
      batch_size=2;
      int num_batches = 128;
      for(int i=0;i<num_batches;i+=2) {
          int start_index = i;
          int level_start = 8;
          int level_end = 2;

          bptr_t bptr;
          bptr.level_size = level_size;
          bptr.batch_size = batch_size;
          bptr.start_index = start_index;
          bptr.record_num = record_num;
          bptr.level_start = level_start;
          bptr.level_end = level_end;

          finfo->f_pbptr = &bptr;

          int x1 = rowOfIntsX[record_num][start_index];
          int y1 = rowOfIntsY[record_num][start_index];

          int x2 = rowOfIntsX[record_num][start_index+1];
          int y2 = rowOfIntsY[record_num][start_index+1];

          int x3 = rowOfIntsX[record_num][start_index+level_size/2];
          int y3 = rowOfIntsY[record_num][start_index+level_size/2];

          int x4 = rowOfIntsX[record_num][start_index+level_size/2+1];
          int y4 = rowOfIntsY[record_num][start_index+level_size/2+1];

          // single atomic unit to be called as such
          d1 = bfly2(x1, y1, x2, y2, start_index, record_num);
          d2 = bfly3(x3, y3, x4, y4, start_index+level_size/4, record_num);

          BFlyNode bflynode;

          bflynode.d1 = d1;
          bflynode.d2 = d2;

          bflynode.x1 = x1;
          bflynode.y1 = y1;
          bflynode.x2 = x2;
          bflynode.y2 = y2;

          finfo->bflynode_ptr = &bflynode;

          update_state(finfo);

          end_run();
      }

}


void update_state(struct func_info_t *finfo) {

   l = malloc(sizeof(struct ilist));
   l->fi = finfo;
      /* insert the new element into the list while keeping it sorted */
   SGLIB_SORTED_LIST_ADD(struct ilist, the_list, l, ILIST_COMPARATOR, next_ptr);

   allworkdone = false;
}

void *progress_dft(void *t) {

   long my_id = (long)t;
   std::cout <<   "my_id ="  << my_id << std::endl;
 /*
  Lock mutex and wait for signal.  Note that the pthread_cond_wait routine
  will automatically and atomically unlock mutex while it waits. 
  Also, note that if COUNT_LIMIT is reached before this routine is run by
  the waiting thread, the loop will be skipped to prevent pthread_cond_wait
  from never returning.
  */
   while(dft_in_progress) {
  
       while (allworkdone) {
           // pthread_cond_wait(&count_threshold_cv, &finfo_mutex);
           timespec tspec1, tspec2;
           tspec1.tv_sec = 0;
           tspec1.tv_nsec = 10000;
           nanosleep(&tspec1, &tspec2);
       }
   

      // do some work
      pthread_mutex_lock(&finfo_mutex);
      SGLIB_LIST_MAP_ON_ELEMENTS(struct ilist, the_list, ll, next_ptr, {

           // already sorted on record_num
           struct func_info_t *func_iptr = ll->fi;
           int rec_num = func_iptr->f_pbptr->record_num;
           int start_index = func_iptr->f_pbptr->start_index;
           int level_size = func_iptr->f_pbptr->level_size;

           BFlyNode *bfly_ptr = func_iptr->bflynode_ptr;

           dfactors[rec_num][start_index] = bfly_ptr->d1;
           dfactors[rec_num][start_index+(level_size/2)] = bfly_ptr->d2;

      });
       

      allworkdone = true;
      pthread_mutex_unlock(&finfo_mutex);

   }

}



void *stage_func(void *stage) {

      int STOP_TOKEN = 1;
      stage_t *stg = stage;
      int stage_num = stg->stage_num;
      while(dft_in_progress) {

           int randrow = rand_interval(0,  m_cols);

           int e=0;
           int e2 = 0;
           double pfac;
           int kernsize = KERNEL_SIZE_FOR_STAGE(stage_num);

           int kernsizeMax = KERNEL_SIZE_MAX_FOR_STAGE(stage_num);
 
           pfac = 1;
           int pnum = 0;
           while(e<LEVEL_SIZE) {
               pfac *= dfactors[randrow][e]*(layerMask[kernsize-1])[e] * dfactors[randrow][e+2]*(layerMask[kernsize-1])[e+2]; 
               if(pfac != 0) {
                   double d1 = bfly2(dfactors[randrow][e], dfactors[randrow][e+2]); 
                   double d128 =  bfly3(dfactors[randrow][e+128], dfactors[randrow][e+130]); 
                   dfactors[randrow][e] = d1;
                   dfactors[randrow][e+128] = d128;
                   dfactors[randrow][e+2] = STOP_TOKEN;
                   dfactors[randrow][e+130] = STOP_TOKEN;
                   pnum++;

                   if((pnum*kernsize)/8 == 1) {
                      pipe_send( stg->next, pnum);
                      pnum = 0;
                      pfac = 1;
                      e2 = 0;
                   } 
                   
               }
                   e = e+kernsize;
           }


      }

}


/*
  This is the crunch time for the DFT. The level 2 dft has been computed and the 
  double values placed in the dfactor buffer. The worker threads are running and 
  must scan the dfactors buffer for entries placed there by the first level level 2 dft run.

  both rows and columns must be scanned. each worker thread has a range of rows to work with.
  inside a row, the entries must be grouped pairwise and then the level 4 bfly calculated
  and the results placed back in the buffer itself although in a different position. The position alone 
  determines what layer of dft is to be run next. thus the same row may contain some values still requiring 
  level 4 dft to be run whereas others may have progressed to level 8, 16 and so on. 

  scanning for pairs is first in sets of 2  and then in sets of 4, 8 etc. depending on which layer of dft is running.
  for a level 4 dft, 4 pairs are needed.
    (01), (23), (45), (67) or (64,65), (66,67), (68,69), (70, 71) 
   it is a double array and we will only see the results of the bfly computation. hence we will see
     0:d1,   2:d2,   4:d3,  6:d4   
    thus only the position where data is determines the level of dft that is running
    as 2 is filled, level 2 is active and so level 4 bfly is computed and result placed in 0 and 
    level 2 is filled with STOP word e.g 99. 
    level 4 is filled and level 6 is blank. that could be because level 6 hasn't been computed and filled yet.
    0: d1  2:99    4:d3    6:   8:d
    0:d1   2:99    4:d3    6:d4  8:d

    now, 6 has arrived. level 2 dft is computed and the state changes to
    0:d1  2:99     4:d2    6:99  8:  and so on
    another thread see 0 and 4 is filled and runs level 4 dft on them
    0: d1  2:99   4:99    6:99   8:  
    and so on and so forth.

    when a row is fully done, is is marked as done in the check buffer. threads must check this check 
    buffer before they start scanning rows.
    when all rows are done or upto a buffer maximum is reached, the dft operation is marked as complete, the 
    threads are destroyed  and the results returned to caller program.
*/
double _Complex bfly2(int x1, int y1, int x2, int y2, int num, int record_num) {

    double _Complex twfac = get_twiddle(num);
    double d1 = m_data[record_num][x1] * m_data[record_num][y2];
    double d2 = m_data[record_num][x2] * m_data[record_num][y1];

    twProdFactors[record_num][num] = twfac * d2;
    double _Complex d3 = d1 + twProdFactors[record_num][num];

    return d3;
}

double _Complex bfly3(int x1, int y1, int x2, int y2, int num, int record_num) {

    double _Complex twfac = get_twiddle(num);
    double d1 = m_data[record_num][x1] * m_data[record_num][y2];
    double d2 = m_data[record_num][x2] * m_data[record_num][y1];

    double _Complex d3 = d1 - twProdFactors[0][num];

    return d3;
}



void fft() {


    printf(" enter fft numrows m = \n", m_rows);
    int NUM_COLS = log2(m_cols);

    printf(" enter fft numrows  = \n", NUM_COLS);

    //double ** rowOfDoubles =  malloc(sizeof(double *) * NUM_COLS);
    int ** rowOfIntsX =  malloc(sizeof(int *) * NUM_COLS);
    int ** rowOfIntsY =  malloc(sizeof(int *) * NUM_COLS);

    //for(int k=0;k<NUM_COLS;k++) {
    //    rowOfDoubles[k] = malloc(sizeof(double) * m_size);
    //}

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


}

const char * generate_unique_id() {

    int ival = 0;
    char *str_id = malloc(sizeof(char)*17);
    for(int i=0;i<17;i++) {
        int rand1 = rand() % 62; 

        int rmax = rand1+17;
        if(rand1 > 45) {
            rmax = 62;
        }
        ival = rand_interval(rand1, rmax);

        strcat(chars[ival], str_id);;
    }

    printf(" std id = %s\n", str_id);

}

unsigned int rand_interval(unsigned int min, unsigned int max)
{
    int r;
    const unsigned int range = 1 + max - min;
    const unsigned int buckets = RAND_MAX / range;
    const unsigned int limit = buckets * range;

    /* Create equal size buckets all in a row, then fire randomly towards
     * the buckets until you land in one of them. All buckets are equally
     * likely. If you land off the end of the line of buckets, try again. */
    do
    {
        r = rand();
    } while (r >= limit);

    return min + (r / buckets);
}


    /*
     iptr_t *ptrt = get_iptr_info(name);
     if(iptr  == NULL) {
        const char *err_msg="func " + name + " not found";
        return 100;
     }

    --counters[ptrt->iptr];

    if(ptrt->callbackFunc != NULL)
       callbackFunc();
    */
//}

/*
registry::call_wrap(int x, double d, func foo) {
 
    before();

    new Thread() {
         Object o;
         void run() {
           o = foo();
         }

         Object get() {
            return o;
         }
    }

   after();

}


registry::after(Object o) {
   this->counter--;

   list objects;

   o.level;
   o.wsize;
   o.batch_size;
   o.batch_num;
   o.id; 
   o.sort_id;

   objects::put o

}


registry::compareTo(Object o1, Object o2) {

      if(matches(o1, o2)) {
          Object o3 = foo2(); 
          objects::put o3;
      }

}


registry::matches(Object o1, Object o2) {

         if(o1.level == o2.level &&
            o1.xarr == o2.xarr
}
 */
