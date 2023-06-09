package main

import "util"
import "fmt"
//import "common"

 type IntegerItem struct {
//     util.ListItem
     x int
 }

  //fwd decls
 
    var  Ulist  = util.NewList()


 func (item IntegerItem) Visit2() {
      fmt.Println("IntegerItem  is visited")
 }

 func NewIntegerItem(x int) IntegerItem {
   //  val := IntegerItem{ util.NewListItem(""), x , }
     val := IntegerItem{ x , }
     return val
 }

 func (item IntegerItem) String() string {
      fmt.Println("IntegerItem visited")
    return "";
 }




