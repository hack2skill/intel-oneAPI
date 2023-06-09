package util

import "fmt"
import "common"


type List struct {

  store []common.ListItemVisit

}

func NewList() *List {

  var listx List
  return &listx

}

type ErrSizeExceeded float64

func (e ErrSizeExceeded) Error() string {
    fmt.Println(float64(e));
	
	return ""
}


type ListInit interface {
      addMe()
      newfuncs()
}

type ListItem struct {
     data string
}

func NewListItem(data string) ListItem {
     return ListItem{ data, }
}


func (item ListItem) Visit2() {
         fmt.Println( "List item visited"  );
}

func (item ListItem) String() string {
         fmt.Println( "ListItem visited"  );
     return ""
}

type T struct {
}


/*
func (item ListItem) newfuncs(n int, fns []func()) {
    funcs =  make(ListItemFunc, 2);

    for f, g := range fns {
       funcs  <- g
    }
}

func (item ListItem, deferred bool) visit() {

     for i, v := range funcs {
           if deferred {
           defer   (<- funcs)()
           } else {
              (<- funcs)()
           }
     }

}

*/



func  mainmain() {

   NewList().Append(NewListItem("Hello TEST"))

}


func (list *List) Append(item common.ListItemVisit) *List {

    list.store = append(list.store, item)
    return list

}


func (list *List) At(x int) (common.ListItemVisit, error) {

    var err  ErrSizeExceeded = 99.0
    if x >= len(list.store) {
        itemerr := NewListItem("")
        return itemerr, err
    }

    err  = 0.0
    return list.store[x], err

}


func (list *List) Set(x int, d ListItem) error {

    var err  ErrSizeExceeded = 99.0
    if x >= len(list.store) {
        return err
    }

    list.store[x] = d

    err = 0.0;
    return err;
}



func (list *List) Len() int {

   return len(list.store);

}

func (list *List) Size() int {

   return cap(list.store);

}

func (list *List) Print() int {

   fmt.Println("[ ")
   for _, v := range  list.store {
          v.Visit2()
          fmt.Print(", ")
            
   }
          fmt.Println("] ")

   return 0;

}
