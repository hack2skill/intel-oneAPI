/*
 * Internal structure describing a "stage" in the
 * pipeline. One for each thread, plus a "result
 * stage" where the final thread can stash the value.
 */
typedef struct stage_tag {
    char               * stage_name;
    int                  stage_num;
    int                  base_radix;
    pthread_mutex_t     mutex;          /* Protect data */
    pthread_cond_t      avail;          /* Data available */
    pthread_cond_t      ready;          /* Ready for data */
    int                 data_ready;     /* Data present */
    long                data;           /* Data to process */
    pthread_t           thread;         /* Thread for stage */
    struct stage_tag    *next;          /* Next stage */
} stage_t;

/*
 * External structure representing the entire
 * pipeline.
 */
typedef struct pipe_tag {
    int            run_number;
    int                 row;
    pthread_mutex_t     mutex;          /* Mutex to protect pipe */
    stage_t             *head;          /* First stage */
    stage_t             *tail;          /* Final stage */
    int                 stages;         /* Number of stages */
    int                 active;         /* Active data elements */

} pipe_t;

int pipe_send (stage_t *stage, long data);
int pipe_create (pipe_t *pipe, int stages, threadpool tpool);
