package common



type ListItemVisit interface {
      Visit2()
}

type T struct {
     d *float64
}


func NewT(sz int) *T {

    var tInst T
    d := make([]float64, sz) 

    tInst.d = &d[0]

   return &tInst

}

