#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include "sglib.h"

typedef struct finfo {

    int record_num;
    int start_index;

} finfo_t;
struct ilist {
    finfo_t fi;
    struct ilist *next_ptr;
};


#define ILIST_COLUMN_COMPARATOR(e1, e2)  (e1->fi.start_index - e2->fi.start_index)
#define ILIST_COMPARATOR(e1, e2)  (e1->fi.record_num - e2->fi.record_num)

int nums[] = { 1, 7, 5, 10, 2, 1,  2, 7, 5, 1, 2, 10, 7, 5, 1,  5 };
int si[] = {   9, 2, 12, 6, 8, 13, 4, 6, 2, 4, 3, 9,  2, 3, 16, 12 };
int main(int argc, char **argv) {
  int i,a;
  struct ilist *l, *the_list;
  the_list = NULL;
  for (i=1; i<16; i++) {
//    sscanf(argv[i],"%d", &a);

     finfo_t fi;

     fi.record_num = nums[i];
     fi.start_index = si[i];

    l = malloc(sizeof(struct ilist));
    l->fi = fi;
    /* insert the new element into the list while keeping it sorted */
    SGLIB_SORTED_LIST_ADD(struct ilist, the_list, l, ILIST_COMPARATOR, next_ptr);
  }
  SGLIB_LIST_MAP_ON_ELEMENTS(struct ilist, the_list, ll, next_ptr, {
      finfo_t f = ll->fi;
    printf("rnum = %d ", f.record_num);
    printf("si = %d ", f.start_index);
  });
  printf("\n");
  SGLIB_LIST_MAP_ON_ELEMENTS(struct ilist, the_list, ll, next_ptr, {
    free(ll);
  });
  return(0);
}
