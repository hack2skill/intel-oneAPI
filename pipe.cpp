/*
 * pipe.c
 *
 * Simple demonstration of a pipeline. main() is a loop that
 * feeds the pipeline with integer values. Each stage of the
 * pipeline increases the integer by one before passing it along
 * to the next. Entering the command "=" reads the pipeline
 * result. (Notice that too many '=' commands will hang.)
 */
#include <pthread.h>
#include "errors.h"
#include "thpool.h"
#include "pipe.h"


threadpool             *thpools;
threadpool             pool0;
extern void *stage_func(void *);
/*
 * Internal function to send a "message" to the
 * specified pipe stage. Threads use this to pass
 * along the modified data item.
 */
int pipe_send (stage_t *stage, long data)
{
    int status;

    status = pthread_mutex_lock (&stage->mutex);
    if (status != 0)
        return status;
    /*
     * If there's data in the pipe stage, wait for it
     * to be consumed.
     */
    while (stage->data_ready) {
        status = pthread_cond_wait (&stage->ready, &stage->mutex);
        if (status != 0) {
            pthread_mutex_unlock (&stage->mutex);
            return status;
        }
    }

    /*
     * Send the new data
     */
    stage->data = data;
    stage->data_ready = 1;
    status = pthread_cond_signal (&stage->avail);
    if (status != 0) {
        pthread_mutex_unlock (&stage->mutex);
        return status;
    }
    status = pthread_mutex_unlock (&stage->mutex);
    return status;
}

/*
 * The thread start routine for pipe stage threads.
 * Each will wait for a data item passed from the
 * caller or the previous stage, modify the data
 * and pass it along to the next (or final) stage.
 */
void *pipe_stage (void *arg)
{
    stage_t *stage = (stage_t*)arg;
    stage_t *next_stage = stage->next;
    int status;

    status = pthread_mutex_lock (&stage->mutex);
    if (status != 0)
        err_abort (status, "Lock pipe stage");
    while (1) {
        while (stage->data_ready != 1) {
            status = pthread_cond_wait (&stage->avail, &stage->mutex);
            if (status != 0)
                err_abort (status, "Wait for previous stage");
        }


    //    pipe_send (next_stage, stage->data + 1);

        thpool_resume(thpools[stage->stage_num]);

        stage_func(stage);

        stage->data_ready = 0;
        status = pthread_cond_signal (&stage->ready);
        if (status != 0)
            err_abort (status, "Wake next stage");
    }
    /*
     * Notice that the routine never unlocks the stage->mutex.
     * The call to pthread_cond_wait implicitly unlocks the
     * mutex while the thread is waiting, allowing other threads
     * to make progress. Because the loop never terminates, this
     * function has no need to unlock the mutex explicitly.
     */
}


/*
 * External interface to create a pipeline. All the
 * data is initialized and the threads created. They'll
 * wait for data.
 */
int pipe_create (pipe_t *pipe, int stages, threadpool thpool0)
{
    int pipe_index;
    stage_t **link = &pipe->head, *new_stage, *stage;
    int status;

    status = pthread_mutex_init (&pipe->mutex, NULL);
    if (status != 0)
        err_abort (status, "Init pipe mutex");
    pipe->stages = stages;
    pipe->active = 0;

    for (pipe_index = 0; pipe_index <= stages; pipe_index++) {
        new_stage = (stage_t*)malloc (sizeof (stage_t));
        if (new_stage == NULL)
            errno_abort ("Allocate stage");
        status = pthread_mutex_init (&new_stage->mutex, NULL);
        if (status != 0)
            err_abort (status, "Init stage mutex");
        status = pthread_cond_init (&new_stage->avail, NULL);
        if (status != 0)
            err_abort (status, "Init avail condition");
        status = pthread_cond_init (&new_stage->ready, NULL);
        if (status != 0)
            err_abort (status, "Init ready condition");
        new_stage->data_ready = 0;
        new_stage->stage_num = pipe_index;
        *link = new_stage;
        link = &new_stage->next;
    }

    *link = (stage_t*)NULL;     /* Terminate list */
    pipe->tail = new_stage;     /* Record the tail */

    /*
     * Create the threads for the pipe stages only after all
     * the data is initialized (including all links). Note
     * that the last stage doesn't get a thread, it's just
     * a receptacle for the final pipeline value.
     *
     * At this point, proper cleanup on an error would take up
     * more space than worthwhile in a "simple example", so
     * instead of cancelling and detaching all the threads
     * already created, plus the synchronization object and
     * memory cleanup done for earlier errors, it will simply
     * abort.
     */
     
     /* We create thread pools for each stage. We also
        create a pthread for each stage for signalling. We signal the 
        pthread and the pthread signals the thread pool.
        The thread pool for stage 0 first stage is passed as
        parameter. We create the thread pools for all other stages.
     */

    pool0 = thpool0;
    if(pool0 == NULL) {
       errno_abort(" pool 0 not provided");
    }

    thpools = malloc (sizeof(threadpool)*stages);
    int t=0;
    for (   stage = pipe->head;
            stage->next != NULL;
            stage = stage->next) {
        if(t == 0) {
            thpools[0] = thpool0;
            thpool_add_work(pool0, (void*)stage_func, (void *)stage);
        }
        else {
            thpools[t] = thpool_init(5);
            thpool_add_work(thpools[t], (void*)stage_func, (void *)stage);
            thpool_pause(thpools[t]);
        }
        t++;
    }

    for (   stage = pipe->head;
            stage->next != NULL;
            stage = stage->next) {
        status = pthread_create (
            &stage->thread, NULL, pipe_stage, (void*)stage);
        if (status != 0)
            err_abort (status, "Create pipe stage");
    }
    return 0;
}

/*
 * External interface to start a pipeline by passing
 * data to the first stage. The routine returns while
 * the pipeline processes in parallel. Call the
 * pipe_result return to collect the final stage values
 * (note that the pipe will stall when each stage fills,
 * until the result is collected).
 */
int pipe_start (pipe_t *pipe, long value)
{
    int status;

    status = pthread_mutex_lock (&pipe->mutex);
    if (status != 0)
        err_abort (status, "Lock pipe mutex");
    pipe->active++;
    status = pthread_mutex_unlock (&pipe->mutex);
    if (status != 0)
        err_abort (status, "Unlock pipe mutex");
    pipe_send (pipe->head, value);
    return 0;
}

/*
 * Collect the result of the pipeline. Wait for a
 * result if the pipeline hasn't produced one.
 */
int pipe_result (pipe_t *pipe, long *result)
{
    stage_t *tail = pipe->tail;
    long value;
    int empty = 0;
    int status;

    status = pthread_mutex_lock (&pipe->mutex);
    if (status != 0)
        err_abort (status, "Lock pipe mutex");
    if (pipe->active <= 0)
        empty = 1;
    else
        pipe->active--;

    status = pthread_mutex_unlock (&pipe->mutex);
    if (status != 0)
        err_abort (status, "Unlock pipe mutex");
    if (empty)
        return 0;

    pthread_mutex_lock (&tail->mutex);
    while (!tail->data_ready)
        pthread_cond_wait (&tail->avail, &tail->mutex);
    *result = tail->data;
    tail->data_ready = 0;
    pthread_cond_signal (&tail->ready);
    pthread_mutex_unlock (&tail->mutex);    
    return 1;
}

/*
 * The main program to "drive" the pipeline...
 */
int main (int argc, char *argv[])
{
    pipe_t my_pipe;
    long value, result;
    int status;
    char line[128];

    threadpool thpool5 = thpool_init(2);
    pipe_create (&my_pipe, 10, thpool5);
    printf ("Enter integer values, or \"=\" for next result\n");

    while (1) {
        printf ("Data> ");
        if (fgets (line, sizeof (line), stdin) == NULL) exit (0);
        if (strlen (line) <= 1) continue;
        if (strlen (line) <= 2 && line[0] == '=') {
            if (pipe_result (&my_pipe, &result))
                printf ("Result is %ld\n", result);
            else
                printf ("Pipe is empty\n");
        } else {
            if (sscanf (line, "%ld", &value) < 1)
                fprintf (stderr, "Enter an integer value\n");
            else
                pipe_start (&my_pipe, value);
        }
    }
}
