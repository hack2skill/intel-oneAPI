package nnet

import (
        "deck"
        "fmt"



	"math"

	"gonum.org/v1/gonum/blas"
	"gonum.org/v1/gonum/blas/blas64"
	"gonum.org/v1/gonum/lapack/lapack64"
)


type Network struct {
}

type  StepDeck struct {
    deck.Deck
}


type MatMul struct {
    deck.Step

}

func (m MatMul) execute () {

         fmt.Printf("matmul execute\n")
}

type MultiMatMul struct {
    MatMul

    num_iters int

}

func (m MultiMatMul) execute () {
         fmt.Printf("multimatmul execute\n")

}


type ConvolveOp struct {
    deck.Step
}

func (m ConvolveOp) execute () {
         fmt.Printf("convolveop execute\n")

}

type LUDecomp struct {
    deck.Step
}

func (m LUDecomp) execute () {
         fmt.Printf("ludecomp execute\n")

}

type EigenDecomp struct {
    deck.Step
}

func (m EigenDecomp) execute () {
         fmt.Printf("eigendecomp execute\n")

}


func NewMatMul(name string, id int, xdim int, ydim int, data *float64, x2dim int, y2dim int, kernel *float64) MatMul {

    var m MatMul

    m.Step = deck.NewStep(name, id, xdim, ydim)

    return m
}

func NewMultiMatMul(name string, id int, xdim int, ydim int, data *float64, x2dim int, y2dim int, kernel *float64,  num_iters int) MultiMatMul {
    var mm MultiMatMul

    mm.MatMul = NewMatMul(name, id, xdim, ydim)

    mm.num_iters = num_iters

    return mm

}

func NewLUDecomp(name string, id int, xdim int, ydim int, data *float64) LUDecomp {
    var lud LUDecomp

    lud.Step = deck.NewStep(name, id, xdim, ydim)

    return lud 

}

func NewEigenDecomp(name string, id int, xdim int, ydim int, data *float64) EigenDecomp {
    var eig EigenDecomp

    eig.Step = deck.NewStep(name, id, xdim, ydim)

    return  eig

}

func NewConvolveOp(name string, id int, xdim int, ydim int, data *float64) ConvolveOp {
    var conv ConvolveOp

    conv.Step = deck.NewStep(name, id, xdim, ydim)

    return conv 

}

func NewStepDeck() StepDeck {

   var stepDeck *StepDeck
   stepDeck = &StepDeck{}
   stepDeck.Deck = deck.NewDeck()

   return *stepDeck;

}

func (d StepDeck) AddStep(s1 deck.Step) {
   d.Deck.AddStep(s1)
}

func (d StepDeck) AddStepOp(s1 deck.StepOp) {
   d.Deck.AddStepOp(s1)
}

func (d StepDeck) RemoveStep(s1 deck.Step) {
    d.Deck.RemoveStep(s1.GetId())
}

func (d StepDeck) Clear() {
    d.Deck.Clear()
}

func (d StepDeck) Run() {
    fmt.Printf("stepdeck run called. calling runTillEnd()\n ")
    d.RunTillEnd()
}

func (d StepDeck) RunTillEnd() {

         fmt.Printf("stepdeck runtillend called\n")

          it := d.Deck.GetSet().Iterator()
          for(it.Next()) {

             value := it.Value()

            switch v := value.(type) {
                    case MatMul:
                            mmul :=  value.(MatMul)
                            mmul.execute()
                    case MultiMatMul:
                            multimmul :=  value.(MultiMatMul)
                            multimmul.execute()
                    case LUDecomp:
                            lucomp2 :=  value.(LUDecomp)
                            lucomp2.execute()
                    case EigenDecomp:
                            eigcomp2 :=  value.(EigenDecomp)
                            eigcomp2.execute()
                    case ConvolveOp:
                            convOp :=  value.(ConvolveOp)
                            convOp.execute()
                    default:
                            fmt.Println("unknown", v)

            }

          }
}

func (nn Network) Build(xdim, ydim int, data *float64, pxdim, pydim int, pdata *float64) {

           /* 
                 Adding vis Step works as the correct Step run gets called.
                 But then iteration over the set fails as type resolves 
                 to interface{} type
           */
           /*
       deck1 := NewStepDeck()

       m1 := NewMatMul("MATMUL", 1 , xdim, ydim, data, pxdim, pydim, pdata)

       m2 :=  NewMultiMatMul("MULTIMATMUL", 2 , xdim, ydim, data, pxdim, pydim, pdata, 26)

       m3 := NewConvolveOp("CONVOLVE_OP", 3 , xdim, ydim, data)

       m4 := NewLUDecompOp("LU_DECOMP", 4 , xdim, ydim, data)

       m5 := NewEigenDecomp("EIGEN_DECOMP", 5 , xdim, ydim, data)

      fmt.Printf("Adding to deck using Step ")

      deck1.AddStep(m1.Step)

      deck1.AddStep(m2.MatMul.Step)

      deck1.AddStep(m3.Step)

      deck1.AddStep(m4.Step)

      deck1.AddStep(m5.Step)

      deck1.Run()
           */

     /* Adding using interface StepOp works fine 
        and we will use that  
      */

      fmt.Printf("Adding to deck using StepOp ")

      deck22 := NewStepDeck()

       var s1, s2, s3 deck.StepOp

       s1 = NewMatMul("MATMUL", 1 , xdim, ydim, data, pxdim, pydim, pdata)

       s2 =  NewMultiMatMul("MULTIMATMUL", 2 , xdim, ydim, data, pxdim, pydim, pdata, 26)

       s3 = NewConvolveOp("CONVOLVE_OP", 3 , xdim, ydim, data) 

       s4 = NewConvolveOp("LU_DECOMP", 3 , xdim, ydim, data) 

       s5 = NewConvolveOp("EIGEN_DECOMP", 3 , xdim, ydim, data) 

      deck22.AddStepOp(s1)

      deck22.AddStepOp(s2)

      deck22.AddStepOp(s3)

      deck22.AddStepOp(s4)

      deck22.AddStepOp(s5)

      deck22.Run()




} 
